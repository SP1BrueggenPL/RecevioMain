from django.db import migrations

# English copy matches what migration 0036 already seeded for all three
# screens (manual/badge/code); Polish is the translation that was missing
# entirely (the kiosk's completion screen always rendered this English text
# regardless of the visitor's selected language — see get_text() on the model).
TEXT_EN = {
    "heading": "Your registration has been successfully completed.",
    "subheading": "The host has been informed about the completion of your registration",
    "body_no_badge": "A badge is not required for visitors who will not access the production area.",
    "footer_note": "You will be redirected to the start screen in a moment...",
}
TEXT_PL = {
    "heading": "Twoja rejestracja została zakończona pomyślnie.",
    "subheading": "Osoba zapraszająca została poinformowana o zakończeniu Twojej rejestracji",
    "body_no_badge": "Identyfikator nie jest wymagany dla gości, którzy nie wchodzą na teren produkcyjny.",
    "footer_note": "Za chwilę nastąpi przekierowanie do ekranu startowego...",
}
BADGE_NOTE_EN = "Your badge sticker will be issued by reception staff."
BADGE_NOTE_PL = "Naklejkę/identyfikator wyda Ci pracownik recepcji."


def backfill(apps, schema_editor):
    CompletionScreenContent = apps.get_model("GuestBook", "CompletionScreenContent")
    for content in CompletionScreenContent.objects.all():
        for field, en_text in TEXT_EN.items():
            setattr(content, f"{field}_en", en_text)
        for field, pl_text in TEXT_PL.items():
            setattr(content, f"{field}_pl", pl_text)
        content.badge_issuance_note_en = BADGE_NOTE_EN
        content.badge_issuance_note_pl = BADGE_NOTE_PL
        content.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("GuestBook", "0041_completionscreencontent_i18n"),
    ]

    operations = [
        migrations.RunPython(backfill, noop),
    ]
