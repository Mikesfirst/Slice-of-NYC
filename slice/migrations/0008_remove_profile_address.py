# Generated by Django 4.2.1 on 2023-09-10 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slice', '0007_profile_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
    ]
