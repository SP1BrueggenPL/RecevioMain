# Generated for Django 6.0.4

import io

from django.db import migrations, models


def copy_files_to_binary_fields(apps, schema_editor):
    """Best-effort: a file referenced by the old FileField columns might
    still exist on disk right now (e.g. it was uploaded moments before this
    deploy runs). Copy its bytes into the new DB-backed field before the
    old column is dropped below — anything already lost to a previous
    ephemeral-storage wipe (see MEDIA_ROOT in settings.py) simply stays
    lost; there's nothing left on disk to copy.

    Deliberately adds new columns and copies into them rather than
    ALTER-ing the old varchar columns in place: on Postgres, ALTER COLUMN
    ... TYPE bytea silently reinterprets the *path string's own bytes* as
    the image content instead of reading the file it points to — tested
    directly against Postgres while writing this migration. Add+copy+drop
    +rename avoids that entirely.
    """
    Visitor = apps.get_model("GuestBook", "Visitor")
    AdminProfile = apps.get_model("GuestBook", "AdminProfile")

    for visitor in Visitor.objects.all().iterator():
        update_fields = []
        if visitor.signed:
            try:
                with visitor.signed.open("rb") as f:
                    data = f.read()
            except (OSError, ValueError):
                data = b""
            if data:
                visitor.signed_data = data
                update_fields.append("signed_data")
        if visitor.host_signature:
            try:
                with visitor.host_signature.open("rb") as f:
                    data = f.read()
            except (OSError, ValueError):
                data = b""
            if data:
                visitor.host_signature_data = data
                update_fields.append("host_signature_data")
        if update_fields:
            visitor.save(update_fields=update_fields)

    for profile in AdminProfile.objects.all().iterator():
        if not profile.signature:
            continue
        try:
            with profile.signature.open("rb") as f:
                data = f.read()
        except (OSError, ValueError):
            data = b""
        if not data:
            continue
        content_type = "image/png"
        try:
            from PIL import Image
            fmt = Image.open(io.BytesIO(data)).format
            if fmt:
                content_type = f"image/{fmt.lower()}"
        except Exception:
            pass
        profile.signature_data = data
        profile.signature_content_type = content_type
        profile.save(update_fields=["signature_data", "signature_content_type"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("GuestBook", "0047_host_alphabetical_ordering"),
    ]

    operations = [
        migrations.AddField(
            model_name="visitor",
            name="signed_data",
            field=models.BinaryField(blank=True, default=b""),
        ),
        migrations.AddField(
            model_name="visitor",
            name="host_signature_data",
            field=models.BinaryField(blank=True, default=b""),
        ),
        migrations.AddField(
            model_name="adminprofile",
            name="signature_data",
            field=models.BinaryField(blank=True, default=b""),
        ),
        migrations.AddField(
            model_name="adminprofile",
            name="signature_content_type",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
        migrations.RunPython(copy_files_to_binary_fields, noop_reverse),
        migrations.RemoveField(
            model_name="visitor",
            name="signed",
        ),
        migrations.RemoveField(
            model_name="visitor",
            name="host_signature",
        ),
        migrations.RemoveField(
            model_name="adminprofile",
            name="signature",
        ),
        migrations.RenameField(
            model_name="visitor",
            old_name="signed_data",
            new_name="signed",
        ),
        migrations.RenameField(
            model_name="visitor",
            old_name="host_signature_data",
            new_name="host_signature",
        ),
        migrations.RenameField(
            model_name="adminprofile",
            old_name="signature_data",
            new_name="signature",
        ),
    ]
