from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GuestBook', '0030_recipient_sender_package_collected_by_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='Phone number'),
        ),
    ]
