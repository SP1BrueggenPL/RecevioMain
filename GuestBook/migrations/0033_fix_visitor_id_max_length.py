from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('GuestBook', '0032_kiosksettings_adminprofile_printer_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='visitor_id',
            field=models.CharField(
                max_length=20,
                validators=[django.core.validators.RegexValidator(r'^\d{1,20}$', 'ID musi składać się z cyfr.')],
                null=False,
            ),
        ),
    ]
