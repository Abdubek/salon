# Generated by Django 2.0.4 on 2018-04-23 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=20, verbose_name='Номер мобильного'),
        ),
    ]
