# Generated by Django 5.0.4 on 2024-04-15 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkProvisioning', '0011_genericdevice_configuration_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='installation_status',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='planned_install_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
