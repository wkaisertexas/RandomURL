# Generated by Django 3.2.6 on 2021-08-14 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('url', '0002_url_link_string'),
    ]

    operations = [
        migrations.RenameField(
            model_name='destination',
            old_name='destination_url',
            new_name='url',
        ),
    ]