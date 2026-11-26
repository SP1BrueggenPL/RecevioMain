from django.db import migrations

# Without this, the "Recevio_SupportCenter_Reception" checkbox never appears
# on the Users page — Group.objects.filter(name__in=ALLOWED_GROUPS) only
# returns rows that already exist (same gotcha fixed for Recevio_Reservation
# in 0044_seed_recevio_reservation_group.py).
GROUP_NAME = "Recevio_SupportCenter_Reception"


def seed(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name=GROUP_NAME)


def unseed(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name=GROUP_NAME).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("GuestBook", "0048_signatures_in_database"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
