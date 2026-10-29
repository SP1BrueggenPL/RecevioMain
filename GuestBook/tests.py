import shutil
import tempfile
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate

from GuestBook.models import (
    AdminProfile,
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
from GuestBook.backends import ChipPinBackend
from GuestBook.forms import VisitorForm
from GuestBook.mail_service import send_pending_package_reminder
from GuestBook.views import _build_package_registered_email, _match_masked_name, _mark_package_issued


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


class PackageLocationTests(TestCase):
    def setUp(self):
        self.sender = Sender.objects.create(name="Test Sender")
        self.recipient = Recipient.objects.create(name="Izabela Benicka", email="r@example.com")

    def test_defaults_to_main_office(self):
        pkg = Package.objects.create(sender=self.sender, recipient=self.recipient, code="BXDEFAULT1")
        self.assertEqual(pkg.location, Package.Location.MAIN_OFFICE)
        self.assertEqual(pkg.location_email_phrase(), "recepcji biura głównego Brüggen")

    def test_social_building_phrase(self):
        pkg = Package.objects.create(
            sender=self.sender, recipient=self.recipient, code="BXSOCIAL1",
            location=Package.Location.SOCIAL_BUILDING,
        )
        self.assertEqual(pkg.location_email_phrase(), "recepcji budynku socjalnego Brüggen")


class PackageRegisteredEmailTests(TestCase):
    def setUp(self):
        self.sender = Sender.objects.create(name="Allegro")
        self.recipient = Recipient.objects.create(name="Izabela Benicka", email="r@example.com")

    def test_main_office_subject_and_body(self):
        pkg = Package.objects.create(
            sender=self.sender, recipient=self.recipient, code="BXC2URAHUB",
        )
        subject, body = _build_package_registered_email(pkg)
        self.assertEqual(subject, "Recepcja Brüggen - paczka w paczkomacie: BXC2URAHUB")
        self.assertIn(
            "Dla odbiorcy: Izabela Benicka zarejestrowano paczkę w paczkomacie "
            "recepcji biura głównego Brüggen.",
            body,
        )

    def test_social_building_subject_and_body(self):
        pkg = Package.objects.create(
            sender=self.sender, recipient=self.recipient, code="BXC2URAHUB",
            location=Package.Location.SOCIAL_BUILDING,
        )
        subject, body = _build_package_registered_email(pkg)
        self.assertEqual(subject, "Recepcja Brüggen - paczka w paczkomacie: BXC2URAHUB")
        self.assertIn(
            "Dla odbiorcy: Izabela Benicka zarejestrowano paczkę w paczkomacie "
            "recepcji budynku socjalnego Brüggen.",
            body,
        )


class PendingPackageReminderEmailTests(TestCase):
    def test_reminder_includes_location_phrase(self):
        status = send_pending_package_reminder("r@example.com", [{
            "code": "BXC2URAHUB",
            "sender": "Allegro",
            "delivered_at": timezone.now(),
            "comment": "",
            "location_phrase": "recepcji budynku socjalnego Brüggen",
        }])
        self.assertEqual(status, "sent")
        from django.core import mail
        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertTrue(sent.subject.startswith("Recepcja Brüggen -"))
        self.assertIn("paczkomat: recepcji budynku socjalnego Brüggen", sent.body)

    def test_reminder_falls_back_to_main_office_phrase_when_missing(self):
        status = send_pending_package_reminder("r@example.com", [{
            "code": "BXNOPHRASE",
            "sender": "Allegro",
            "delivered_at": timezone.now(),
            "comment": "",
        }])
        self.assertEqual(status, "sent")
        from django.core import mail
        self.assertIn("paczkomat: recepcji biura głównego Brüggen", mail.outbox[-1].body)


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


def _make_reception_user():
    group, _ = Group.objects.get_or_create(name="Recevio_Reception")
    user = User.objects.create_user(f"receptionuser{User.objects.count()}", password="pw")
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

    def test_plain_user_cannot_create_reservation_code(self):
        User.objects.create_user("plainuser2", password="pw")
        self.client.login(username="plainuser2", password="pw")
        response = self.client.get(reverse("reservation_code_create"))
        self.assertNotEqual(response.status_code, 200)

    def test_reception_group_can_create_reservation_code(self):
        """Reception runs this page day to day — reuses the existing
        Recevio_Reception group (already manageable from the Users page),
        independent of Recevio_Helpdesk."""
        group, _ = Group.objects.get_or_create(name="Recevio_Reception")
        user = User.objects.create_user("receptionuser", password="pw")
        user.groups.add(group)
        self.client.force_login(user)
        response = self.client.get(reverse("reservation_code_create"))
        self.assertEqual(response.status_code, 200)


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


from django.contrib.auth.hashers import make_password


class ChipPinBackendTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("chipuser", password="unused")
        self.profile = AdminProfile.objects.create(user=self.user, chip_number="12345")

    def test_correct_pin_authenticates(self):
        self.profile.pin_hash = make_password("654321")
        self.profile.save(update_fields=["pin_hash"])
        authenticated = ChipPinBackend().authenticate(None, chip_number="12345", pin="654321")
        self.assertEqual(authenticated, self.user)

    def test_wrong_pin_fails(self):
        self.profile.pin_hash = make_password("654321")
        self.profile.save(update_fields=["pin_hash"])
        self.assertIsNone(ChipPinBackend().authenticate(None, chip_number="12345", pin="000000"))

    def test_no_pin_set_yet_fails(self):
        self.assertIsNone(ChipPinBackend().authenticate(None, chip_number="12345", pin="654321"))

    def test_unknown_chip_number_does_not_crash(self):
        self.assertIsNone(ChipPinBackend().authenticate(None, chip_number="99999", pin="654321"))

    def test_missing_kwargs_returns_none(self):
        self.assertIsNone(ChipPinBackend().authenticate(None))


class ChipLoginFlowTests(KioskRoutingTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user("chipflow", password="unused")
        self.profile = AdminProfile.objects.create(user=self.user, chip_number="54321")

    def test_first_login_sets_pin_and_logs_in(self):
        c = self.client
        resp = c.post(reverse("login"), {"step": "chip", "chip_number": "54321"})
        self.assertContains(resp, 'name="step" value="set_pin"')

        resp = c.post(reverse("login"), {
            "step": "set_pin", "pin": "111222", "pin_confirm": "111222",
        })
        self.assertEqual(resp.status_code, 302)
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.has_pin())
        self.assertIsNotNone(self.profile.pin_set_at)

        self.assertEqual(c.get(reverse("profile")).status_code, 200)

    def test_mismatched_pin_confirmation_is_not_saved(self):
        c = self.client
        c.post(reverse("login"), {"step": "chip", "chip_number": "54321"})
        c.post(reverse("login"), {
            "step": "set_pin", "pin": "111222", "pin_confirm": "999999",
        })
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.has_pin())

    def test_existing_pin_correct_code_logs_in(self):
        self.profile.pin_hash = make_password("777888")
        self.profile.pin_set_at = timezone.now()
        self.profile.save()
        c = self.client
        c.post(reverse("login"), {"step": "chip", "chip_number": "54321"})
        resp = c.post(reverse("login"), {"step": "enter_pin", "pin": "777888"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(c.get(reverse("profile")).status_code, 200)

    def test_existing_pin_wrong_code_does_not_log_in(self):
        self.profile.pin_hash = make_password("777888")
        self.profile.pin_set_at = timezone.now()
        self.profile.save()
        c = self.client
        c.post(reverse("login"), {"step": "chip", "chip_number": "54321"})
        c.post(reverse("login"), {"step": "enter_pin", "pin": "000000"})
        # still anonymous -> @login_required bounces to login
        self.assertEqual(c.get(reverse("profile")).status_code, 302)

    def test_unknown_chip_number_does_not_log_in(self):
        c = self.client
        c.post(reverse("login"), {"step": "chip", "chip_number": "00000"})
        self.assertEqual(c.get(reverse("profile")).status_code, 302)

    def test_superuser_login_redirects_to_django_admin(self):
        su = User.objects.create_superuser("superchip", "s@example.com", "unused")
        AdminProfile.objects.create(user=su, chip_number="90000")
        c = self.client
        c.post(reverse("login"), {"step": "chip", "chip_number": "90000"})
        resp = c.post(reverse("login"), {
            "step": "set_pin", "pin": "135790", "pin_confirm": "135790",
        })
        self.assertRedirects(resp, "/nimda/", fetch_redirect_response=False)


class ResetAuthorizationCodeTests(KioskRoutingTestCase):
    def setUp(self):
        super().setUp()
        self.admin = _make_helpdesk_user()
        self.client.force_login(self.admin)
        self.target_user = User.objects.create_user("resetme", password="unused")
        self.profile = AdminProfile.objects.create(
            user=self.target_user, chip_number="11111",
            pin_hash=make_password("222222"), pin_set_at=timezone.now(),
        )

    def test_reset_clears_pin(self):
        resp = self.client.post(
            reverse("helpdesk_user_edit", args=[self.target_user.pk]),
            {"action": "reset_pin"},
        )
        self.assertEqual(resp.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.pin_hash, "")
        self.assertIsNone(self.profile.pin_set_at)

    def test_user_must_set_new_pin_after_reset(self):
        self.client.post(
            reverse("helpdesk_user_edit", args=[self.target_user.pk]),
            {"action": "reset_pin"},
        )
        c2 = self.client
        resp = c2.post(reverse("login"), {"step": "chip", "chip_number": "11111"})
        self.assertContains(resp, 'name="step" value="set_pin"')


class ChipNumberAssignmentTests(KioskRoutingTestCase):
    def setUp(self):
        super().setUp()
        self.admin = _make_helpdesk_user()
        self.client.force_login(self.admin)
        self.user_a = User.objects.create_user("usera", password="unused")
        self.user_b = User.objects.create_user("userb", password="unused")
        AdminProfile.objects.create(user=self.user_a, chip_number="33333")

    def test_cannot_assign_duplicate_chip_number(self):
        self.client.post(
            reverse("helpdesk_user_edit", args=[self.user_b.pk]),
            {"action": "update", "chip_number": "33333"},
        )
        profile_b, _ = AdminProfile.objects.get_or_create(user=self.user_b)
        self.assertNotEqual(profile_b.chip_number, "33333")

    def test_invalid_chip_number_format_is_rejected(self):
        self.client.post(
            reverse("helpdesk_user_edit", args=[self.user_b.pk]),
            {"action": "update", "chip_number": "abc12"},
        )
        profile_b, _ = AdminProfile.objects.get_or_create(user=self.user_b)
        self.assertNotEqual(profile_b.chip_number, "abc12")

    def test_valid_chip_number_is_saved(self):
        self.client.post(
            reverse("helpdesk_user_edit", args=[self.user_b.pk]),
            {"action": "update", "chip_number": "44444"},
        )
        profile_b, _ = AdminProfile.objects.get_or_create(user=self.user_b)
        self.assertEqual(profile_b.chip_number, "44444")


class RegistrationMethodLabelI18nTests(KioskRoutingTestCase):
    """The kiosk method-name regression: labels must follow the visitor's
    selected language again (see RegistrationMethod.get_label)."""

    def test_get_label_prefers_requested_language(self):
        method = RegistrationMethod.objects.get(slug="badge")
        method.label_pl = "Identyfikator"
        method.label_en = "Badge"
        method.save(update_fields=["label_pl", "label_en"])
        self.assertEqual(method.get_label("pl"), "Identyfikator")
        self.assertEqual(method.get_label("en"), "Badge")

    def test_get_label_falls_back_to_legacy_label_when_blank(self):
        method = RegistrationMethod.objects.get(slug="badge")
        method.label_pl = ""
        method.label_en = ""
        method.label = "Badge"
        method.save(update_fields=["label_pl", "label_en", "label"])
        self.assertEqual(method.get_label("pl"), "Badge")

    def test_choose_method_view_renders_polish_label(self):
        RegistrationMethod.objects.filter(slug="manual").update(
            label_pl="Formularz tożsamości", label_en="Identification form",
        )
        session = self.client.session
        session[settings.LANGUAGE_COOKIE_NAME] = "pl"
        session.save()
        response = self.client.get(reverse("choose_method"))
        self.assertContains(response, "Formularz tożsamości")
        self.assertNotContains(response, "Identification form")

    def test_choose_method_view_renders_english_label(self):
        RegistrationMethod.objects.filter(slug="manual").update(
            label_pl="Formularz tożsamości", label_en="Identification form",
        )
        session = self.client.session
        session[settings.LANGUAGE_COOKIE_NAME] = "en"
        session.save()
        response = self.client.get(reverse("choose_method"))
        self.assertContains(response, "Identification form")
        self.assertNotContains(response, "Formularz tożsamości")


class VisitorFormKeyboardClassTests(TestCase):
    """The kiosk's on-screen keyboard only binds to input.kb-alpha (see
    kiosk/_virtual_keyboard.html) — VisitorForm must put that class on its
    free-text fields for the keyboard to appear on the guest-details form."""

    def test_text_fields_get_kb_alpha_class(self):
        form = VisitorForm()
        for name in ("first_name", "last_name", "phone", "other_company", "other_purpose"):
            self.assertIn("kb-alpha", form.fields[name].widget.attrs.get("class", ""))

    def test_non_text_fields_do_not_get_kb_alpha_class(self):
        form = VisitorForm()
        for name in ("factory", "host", "no_company", "visit_purpose_choice"):
            self.assertNotIn("kb-alpha", form.fields[name].widget.attrs.get("class", ""))


class ReservationManagementTests(KioskRoutingTestCase):
    def setUp(self):
        super().setUp()
        self.reception = _make_reception_user()
        self.client.force_login(self.reception)
        self.reservation = Reservation.objects.create(
            user=self.reception,
            visitor_first_name="Jan",
            visitor_last_name="Kowalski",
            phone="123456789",
            factory=False,
            date=timezone.now().date(),
            status="sent",
        )
        self.code = ReservationCode.objects.create(reservation=self.reservation)
        self.code.usage_count = 2
        self.code.save(update_fields=["usage_count"])

    def test_reset_usage_zeroes_counter(self):
        resp = self.client.post(reverse("reservation_code_reset_usage", args=[self.code.pk]))
        self.assertEqual(resp.status_code, 302)
        self.code.refresh_from_db()
        self.assertEqual(self.code.usage_count, 0)

    def test_reset_usage_requires_reservation_permission(self):
        User.objects.create_user("plainuser3", password="pw")
        self.client.logout()
        self.client.login(username="plainuser3", password="pw")
        resp = self.client.post(reverse("reservation_code_reset_usage", args=[self.code.pk]))
        self.assertNotEqual(resp.status_code, 200)
        self.code.refresh_from_db()
        self.assertEqual(self.code.usage_count, 2)

    def test_cancel_sets_status_cancelled(self):
        resp = self.client.post(reverse("reservation_cancel", args=[self.reservation.pk]))
        self.assertEqual(resp.status_code, 302)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, "cancelled")
        self.assertIsNotNone(self.reservation.cancelled_at)

    def test_helpdesk_can_also_cancel(self):
        self.client.logout()
        self.client.force_login(_make_helpdesk_user())
        resp = self.client.post(reverse("reservation_cancel", args=[self.reservation.pk]))
        self.assertEqual(resp.status_code, 302)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, "cancelled")

    def test_completed_reservation_cannot_be_cancelled(self):
        self.reservation.status = "completed"
        self.reservation.save(update_fields=["status"])
        self.client.post(reverse("reservation_cancel", args=[self.reservation.pk]))
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, "completed")


class ComingVisitorsViewTests(KioskRoutingTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(_make_reception_user())

    def test_lists_upcoming_unarrived_reservation(self):
        reservation = Reservation.objects.create(
            user=_make_reception_user(),
            visitor_first_name="Anna",
            visitor_last_name="Nowak",
            phone="987654321",
            factory=False,
            date=timezone.now().date() + timedelta(days=1),
            status="sent",
        )
        response = self.client.get(reverse("coming_visitors"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Anna")
        self.assertContains(response, "Nowak")


class AccountDeactivationTests(KioskRoutingTestCase):
    def setUp(self):
        super().setUp()
        self.admin = _make_helpdesk_user()
        self.client.force_login(self.admin)
        self.target_user = User.objects.create_user("deactivateme", password="unused")
        self.profile = AdminProfile.objects.create(
            user=self.target_user, chip_number="55555",
            pin_hash=make_password("123456"), pin_set_at=timezone.now(),
        )

    def test_deactivate_sets_is_active_false(self):
        resp = self.client.post(
            reverse("helpdesk_user_edit", args=[self.target_user.pk]),
            {"action": "deactivate"},
        )
        self.assertEqual(resp.status_code, 302)
        self.target_user.refresh_from_db()
        self.assertFalse(self.target_user.is_active)

    def test_reactivate_sets_is_active_true(self):
        self.target_user.is_active = False
        self.target_user.save(update_fields=["is_active"])
        resp = self.client.post(
            reverse("helpdesk_user_edit", args=[self.target_user.pk]),
            {"action": "reactivate"},
        )
        self.assertEqual(resp.status_code, 302)
        self.target_user.refresh_from_db()
        self.assertTrue(self.target_user.is_active)

    def test_cannot_deactivate_own_account(self):
        resp = self.client.post(
            reverse("helpdesk_user_edit", args=[self.admin.pk]),
            {"action": "deactivate"},
        )
        self.assertEqual(resp.status_code, 302)
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)

    def test_deactivated_user_cannot_log_in_via_chip_pin(self):
        self.target_user.is_active = False
        self.target_user.save(update_fields=["is_active"])
        user = ChipPinBackend().authenticate(None, chip_number="55555", pin="123456")
        self.assertIsNone(user)

    def test_active_user_can_still_log_in_via_chip_pin(self):
        user = ChipPinBackend().authenticate(None, chip_number="55555", pin="123456")
        self.assertEqual(user, self.target_user)
