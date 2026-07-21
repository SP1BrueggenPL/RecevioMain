from django.db import migrations


def create_placeholder_recipient(apps, schema_editor):
    Recipient = apps.get_model("GuestBook", "Recipient")
    Recipient.objects.get_or_create(name="BRAK ODBIORCY")


def remove_placeholder_recipient(apps, schema_editor):
    Recipient = apps.get_model("GuestBook", "Recipient")
    Recipient.objects.filter(name="BRAK ODBIORCY").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("GuestBook", "0034_package_label_code_package_label_photo_and_more"),
    ]

    operations = [
        migrations.RunPython(create_placeholder_recipient, remove_placeholder_recipient),
    ]
