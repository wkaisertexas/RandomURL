# Generated by Django 3.2.6 on 2021-09-29 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url', '0003_rename_destination_url_destination_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]