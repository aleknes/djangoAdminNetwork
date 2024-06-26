# Generated by Django 5.0.4 on 2024-04-22 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkProvisioning', '0018_interface'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_number', models.CharField(max_length=255)),
                ('num_of_gigabits', models.PositiveIntegerField()),
                ('num_of_tengigabits', models.PositiveIntegerField()),
            ],
        ),
    ]
