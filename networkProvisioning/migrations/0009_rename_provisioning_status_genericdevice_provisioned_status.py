# Generated by Django 5.0.4 on 2024-04-15 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkProvisioning', '0008_genericdevice_provisioning_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genericdevice',
            old_name='provisioning_status',
            new_name='provisioned_status',
        ),
    ]
