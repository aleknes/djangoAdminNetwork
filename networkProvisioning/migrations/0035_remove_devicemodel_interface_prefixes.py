# Generated by Django 5.0.4 on 2024-04-22 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkProvisioning', '0034_devicemodel_interface_prefixes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicemodel',
            name='interface_prefixes',
        ),
    ]
