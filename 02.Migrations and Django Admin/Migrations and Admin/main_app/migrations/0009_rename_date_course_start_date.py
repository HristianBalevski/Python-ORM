# Generated by Django 4.2.4 on 2023-10-25 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='date',
            new_name='start_date',
        ),
    ]
