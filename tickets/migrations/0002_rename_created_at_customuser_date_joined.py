# Generated by Django 5.2 on 2025-05-03 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='created_at',
            new_name='date_joined',
        ),
    ]
