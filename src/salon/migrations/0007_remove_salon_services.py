# Generated by Django 2.0.4 on 2018-04-24 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0006_auto_20180424_0924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salon',
            name='services',
        ),
    ]
