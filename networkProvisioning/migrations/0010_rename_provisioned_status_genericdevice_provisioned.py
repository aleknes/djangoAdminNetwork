# Generated by Django 5.0.4 on 2024-04-15 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkProvisioning', '0009_rename_provisioning_status_genericdevice_provisioned_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genericdevice',
            old_name='provisioned_status',
            new_name='provisioned',
        ),
    ]
