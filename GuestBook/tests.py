from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from GuestBook.models import Package, Recipient, Sender
from GuestBook.views import _match_masked_name, _mark_package_issued


class MatchMaskedNameLegalSuffixTests(TestCase):
    def test_sa_and_spolka_akcyjna_are_the_same_sender(self):
        db_names = ["AB Spółka Akcyjna"]
        self.assertEqual(_match_masked_name("AB S.A.", db_names), "AB Spółka Akcyjna")

    def test_sp_zoo_and_full_form_are_the_same_sender(self):
        db_names = ["Przykład Spółka z ograniczoną odpowiedzialnością"]
        self.assertEqual(
            _match_masked_name("Przykład Sp. z o.o.", db_names),
            "Przykład Spółka z ograniczoną odpowiedzialnością",
        )

    def test_low_confidence_guess_is_rejected(self):
        db_names = ["Completely Unrelated Company"]
        self.assertIsNone(_match_masked_name("Totally Different Name", db_names))

    def test_empty_name_returns_none(self):
        self.assertIsNone(_match_masked_name("", ["Anything"]))


class MarkPackageIssuedTests(TestCase):
    def setUp(self):
        self.sender = Sender.objects.create(name="Test Sender")
        self.recipient = Recipient.objects.create(name="Test Recipient", email="r@example.com")
        self.user = User.objects.create_user("staffuser", password="pw")
        self.pkg = Package.objects.create(
            sender=self.sender, recipient=self.recipient, code="BXTESTCODE",
        )

    def test_marks_issued_with_registered_recipient(self):
        who = _mark_package_issued(self.pkg, self.recipient, "", self.user, notify=False)
        self.pkg.refresh_from_db()
        self.assertEqual(self.pkg.status, Package.Status.ISSUED)
        self.assertEqual(self.pkg.collected_by, self.recipient)
        self.assertEqual(self.pkg.collected_by_name, "")
        self.assertIsNotNone(self.pkg.issued_at)
        self.assertEqual(who, "Test Recipient")

    def test_marks_issued_with_free_text_name(self):
        who = _mark_package_issued(self.pkg, None, "Jan Kowalski", self.user, notify=False)
        self.pkg.refresh_from_db()
        self.assertIsNone(self.pkg.collected_by)
        self.assertEqual(self.pkg.collected_by_name, "Jan Kowalski")
        self.assertEqual(who, "Jan Kowalski")


class RemindUnpickedPackagesCommandTests(TestCase):
    def setUp(self):
        self.sender = Sender.objects.create(name="Test Sender")
        self.recipient = Recipient.objects.create(name="Test Recipient", email="r@example.com")

    def _make_package(self, code, hours_ago):
        return Package.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            code=code,
            delivered_at=timezone.now() - timedelta(hours=hours_ago),
        )

    def test_reminds_only_packages_older_than_48h_and_marks_them(self):
        old_pkg = self._make_package("BXOLD00001", hours_ago=50)
        recent_pkg = self._make_package("BXNEW00001", hours_ago=2)

        call_command("remind_unpicked_packages")

        old_pkg.refresh_from_db()
        recent_pkg.refresh_from_db()
        self.assertIsNotNone(old_pkg.reminder_sent_at)
        self.assertIsNone(recent_pkg.reminder_sent_at)

    def test_does_not_resend_once_reminder_sent(self):
        pkg = self._make_package("BXOLD00002", hours_ago=72)
        call_command("remind_unpicked_packages")
        pkg.refresh_from_db()
        first_sent_at = pkg.reminder_sent_at
        self.assertIsNotNone(first_sent_at)

        call_command("remind_unpicked_packages")
        pkg.refresh_from_db()
        self.assertEqual(pkg.reminder_sent_at, first_sent_at)
