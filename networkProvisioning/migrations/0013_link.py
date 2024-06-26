# Generated by Django 5.0.4 on 2024-04-22 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkProvisioning', '0012_site_installation_status_site_planned_install_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('side_a_intf', models.CharField(max_length=255)),
                ('side_b_intf', models.CharField(max_length=255)),
                ('side_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='side_a', to='networkProvisioning.site')),
                ('side_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='side_b', to='networkProvisioning.site')),
            ],
        ),
    ]
