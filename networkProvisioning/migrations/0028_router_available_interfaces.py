# Generated by Django 5.0.4 on 2024-04-22 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkProvisioning', '0027_delete_interface_delete_interfacespec'),
    ]

    operations = [
        migrations.AddField(
            model_name='router',
            name='available_interfaces',
            field=models.JSONField(default=0, help_text='Automatically generated from device model when saving'),
            preserve_default=False,
        ),
    ]