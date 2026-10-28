import shutil
import tempfile
from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate

from GuestBook.models import (
    CompletionScreenContent,
    Package,
    Recipient,
    RegistrationMethod,
    RegistrationStage,
    Reservation,
    ReservationCode,
    Sender,
    Visitor,
)
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


def _make_helpdesk_user():
    group, _ = Group.objects.get_or_create(name="Recevio_Helpdesk")
    user = User.objects.create_user("helpdeskuser", password="pw")
    user.groups.add(group)
    return user


class KioskRoutingTestCase(TestCase):
    """All kiosk/panel URLs are wrapped in i18n_patterns(), registered under the
    'pl' prefix (settings.LANGUAGES), while settings.LANGUAGE_CODE is 'pl-pl' —
    a pre-existing mismatch that makes a bare reverse() outside of a request
    context (as in test setup) emit '/pl-pl/...' instead of the '/pl/...' the
    URLconf actually serves. Activating 'pl' explicitly works around that here;
    the settings mismatch itself is a separate, pre-existing issue to flag,
    not something to fix as a side effect of adding tests."""

    def setUp(self):
        super().setUp()
        activate('pl')


class ChooseMethodTemplateTests(KioskRoutingTestCase):
    """The 0036 data migration seeds all four methods active, matching today's
    behavior before this feature existed, so these assert against the seeded state."""

    def test_only_active_methods_render_as_tiles(self):
        RegistrationMethod.objects.filter(slug="badge").update(is_active=False)
        response = self.client.get(reverse("choose_method"))
        self.assertContains(response, reverse("enter_id"))
        self.assertNotContains(response, reverse("enter_badge"))

    def test_unavailable_banner_shown_when_flagged(self):
        response = self.client.get(reverse("choose_method"), {"unavailable": "badge"})
        self.assertContains(response, "currently unavailable")


class DisabledMethodRedirectTests(KioskRoutingTestCase):
    def test_disabled_method_redirects_to_choose_method(self):
        RegistrationMethod.objects.filter(slug="badge").update(is_active=False)
        response = self.client.get(reverse("enter_badge"))
        self.assertRedirects(
            response,
            f"{reverse('choose_method')}?unavailable=badge",
            fetch_redirect_response=False,
        )

    def test_active_method_is_reachable(self):
        RegistrationMethod.objects.filter(slug="badge").update(is_active=True)
        response = self.client.get(reverse("enter_badge"))
        self.assertEqual(response.status_code, 200)


class RegistrationStageToggleTests(KioskRoutingTestCase):
    def setUp(self):
        super().setUp()
        self.user = _make_helpdesk_user()
        self.client.force_login(self.user)

    def test_configurable_stage_can_be_toggled(self):
        stage = RegistrationStage.objects.get(method__slug="badge", stage_key="safety_subflow")
        self.assertTrue(stage.is_configurable)
        response = self.client.post(reverse("registration_stage_toggle"), {
            "stage_id": stage.id, "is_active": "false",
        })
        self.assertEqual(response.status_code, 200)
        stage.refresh_from_db()
        self.assertFalse(stage.is_active)

    def test_locked_stage_cannot_be_toggled(self):
        stage = RegistrationStage.objects.get(method__slug="manual", stage_key="safety_subflow")
        self.assertFalse(stage.is_configurable)
        was_active = stage.is_active
        response = self.client.post(reverse("registration_stage_toggle"), {
            "stage_id": stage.id, "is_active": "false",
        })
        self.assertEqual(response.status_code, 400)
        stage.refresh_from_db()
        self.assertEqual(stage.is_active, was_active)


class RegistrationMethodsPanelPermissionTests(KioskRoutingTestCase):
    def test_anonymous_user_is_redirected(self):
        response = self.client.get(reverse("registration_methods_panel"))
        self.assertEqual(response.status_code, 302)

    def test_non_helpdesk_user_is_denied(self):
        User.objects.create_user("plainuser", password="pw")
        self.client.login(username="plainuser", password="pw")
        response = self.client.get(reverse("registration_methods_panel"))
        self.assertNotEqual(response.status_code, 200)

    def test_helpdesk_user_can_view_panel(self):
        self.client.force_login(_make_helpdesk_user())
        response = self.client.get(reverse("registration_methods_panel"))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_cannot_toggle_method(self):
        method = RegistrationMethod.objects.get(slug="badge")
        response = self.client.post(reverse("registration_method_toggle"), {
            "method_id": method.id, "is_active": "false",
        })
        self.assertNotEqual(response.status_code, 200)
        method.refresh_from_db()
        self.assertTrue(method.is_active)

    def test_anonymous_cannot_create_reservation_code(self):
        response = self.client.get(reverse("reservation_code_create"))
        self.assertEqual(response.status_code, 302)


class CompletionScreenContentTemplateTests(KioskRoutingTestCase):
    def test_print_popup_hidden_by_default(self):
        content = CompletionScreenContent.get_for("manual")
        self.assertFalse(content.print_popup_enabled)
        response = self.client.get(reverse("choose_method"))  # sanity: app boots
        self.assertEqual(response.status_code, 200)

    def test_complete_html_omits_popup_when_disabled(self):
        from django.template.loader import render_to_string
        content = CompletionScreenContent.get_for("manual")
        content.print_popup_enabled = False
        html = render_to_string("kiosk/complete.html", {
            "is_production": True, "visitor_id": 1, "content": content,
        })
        self.assertNotIn("window.open(", html)

    def test_complete_html_includes_popup_when_enabled(self):
        from django.template.loader import render_to_string
        content = CompletionScreenContent.get_for("manual")
        content.print_popup_enabled = True
        html = render_to_string("kiosk/complete.html", {
            "is_production": True, "visitor_id": 1, "content": content,
        })
        self.assertIn("window.open(", html)

    def test_custom_heading_appears_on_screen(self):
        from django.template.loader import render_to_string
        content = CompletionScreenContent.get_for("code")
        content.heading = "Dziękujemy za rejestrację!"
        html = render_to_string("kiosk/complete_code.html", {
            "is_production": False, "content": content,
        })
        self.assertIn("Dziękujemy za rejestrację!", html)


class CodeRegistrationFlowTests(KioskRoutingTestCase):
    """End-to-end walk through the restored 'enter code' method. factory=False
    so the test stays fast and deterministic (no printer/SMTP network calls)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # The signature step writes a real file via default_storage; media/ is
        # tracked in git (guest signature images), so tests must never write
        # there — route uploads to a throwaway directory for this class only.
        cls._media_root = tempfile.mkdtemp(prefix="recevio-test-media-")
        cls._media_root_override = override_settings(MEDIA_ROOT=cls._media_root)
        cls._media_root_override.enable()

    @classmethod
    def tearDownClass(cls):
        cls._media_root_override.disable()
        shutil.rmtree(cls._media_root, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.reservation = Reservation.objects.create(
            user=_make_helpdesk_user(),
            visitor_first_name="Jan",
            visitor_last_name="Kowalski",
            phone="123456789",
            factory=False,
            date=timezone.now().date(),
        )
        self.code = ReservationCode.objects.create(reservation=self.reservation)

    def test_full_chain_creates_visitor_without_sms(self):
        c = self.client

        resp = c.post(reverse("enter_code"), {"code": self.code.code})
        self.assertRedirects(
            resp, reverse("enter_visitor_id_for_code", args=[self.reservation.id]),
        )

        resp = c.post(
            reverse("enter_visitor_id_for_code", args=[self.reservation.id]),
            {"visitor_id": "001"},
        )
        self.assertRedirects(resp, reverse("signature_from_code"))

        resp = c.post(reverse("signature_from_code"), {
            "signature_data": "data:image/png;base64,eA==",
        })
        # finalize_from_code is itself a process-and-redirect view (never
        # returns 200), so don't follow it here — just check where it points.
        self.assertRedirects(
            resp, reverse("finalize_from_code"), fetch_redirect_response=False,
        )

        # This is the view that regressed with @login_required — an anonymous
        # kiosk session must be able to reach it.
        resp = c.get(reverse("finalize_from_code"))
        self.assertRedirects(
            resp, reverse("complete_code", args=[self.reservation.id]),
        )

        resp = c.get(reverse("complete_code", args=[self.reservation.id]))
        self.assertEqual(resp.status_code, 200)

        visitor = Visitor.objects.get(reservation=self.reservation)
        self.assertEqual(visitor.first_name, "Jan")
        self.assertIn(visitor.sms_status, ("skipped", "sent", "timeout", "error"))
        self.assertNotEqual(self.reservation.sms_status, "sent")  # never touched by SMS gateway

        self.code.refresh_from_db()
        self.assertGreaterEqual(self.code.usage_count, 1)
