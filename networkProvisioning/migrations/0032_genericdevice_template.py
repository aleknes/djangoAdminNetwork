# Generated by Django 5.0.4 on 2024-04-22 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkProvisioning', '0031_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericdevice',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='networkProvisioning.template'),
        ),
    ]
