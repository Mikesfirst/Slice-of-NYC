# Generated by Django 4.2.1 on 2023-10-01 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slice', '0009_remove_profile_companionship_profile_hunger_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='personality',
        ),
    ]
