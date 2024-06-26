# Generated by Django 5.0.4 on 2024-04-22 12:49

import networkProvisioning.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkProvisioning', '0030_alter_link_description_alter_link_side_a_intf_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('template_file', models.FileField(storage=networkProvisioning.models.OverwriteStorage(), upload_to='template_files/')),
            ],
        ),
    ]
