from django.db import migrations

# (slug, label_pl, label_en) — label_en matches the English copy the kiosk
# already showed before label_pl/label_en existed (see migration 0036's
# METHODS seed); label_pl is the Polish translation that was lost when the
# kiosk switched from hardcoded {% trans %} strings to this DB-backed label.
LABELS = [
    ("manual", "Formularz tożsamości", "Identification form"),
    ("badge", "Identyfikator", "Badge"),
    ("code", "Kod rejestracyjny", "Registration code"),
    ("exit", "Wyjście (skan identyfikatora)", "Exit (badge scan)"),
]


def backfill(apps, schema_editor):
    RegistrationMethod = apps.get_model("GuestBook", "RegistrationMethod")
    for slug, label_pl, label_en in LABELS:
        RegistrationMethod.objects.filter(slug=slug).update(label_pl=label_pl, label_en=label_en)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("GuestBook", "0039_registrationmethod_label_pl_en"),
    ]

    operations = [
        migrations.RunPython(backfill, noop),
    ]
