# Generated by Django 5.0.4 on 2024-04-22 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkProvisioning', '0021_serialnumber_device_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicemodel',
            name='num_of_gigabits',
        ),
        migrations.RemoveField(
            model_name='devicemodel',
            name='num_of_tengigabits',
        ),
    ]
