# Generated by Django 5.0.4 on 2024-04-22 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkProvisioning', '0013_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='side_a',
        ),
        migrations.RemoveField(
            model_name='link',
            name='side_a_intf',
        ),
        migrations.RemoveField(
            model_name='link',
            name='side_b',
        ),
        migrations.RemoveField(
            model_name='link',
            name='side_b_intf',
        ),
    ]
