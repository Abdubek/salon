# Generated by Django 2.0.4 on 2018-04-23 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffer', '0001_initial'),
        ('services', '0001_initial'),
        ('salon', '0003_auto_20180423_1131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Контакт', 'verbose_name_plural': 'Контакты'},
        ),
        migrations.AddField(
            model_name='salon',
            name='positions',
            field=models.ManyToManyField(blank=True, related_name='salon_staffers', to='staffer.Position', verbose_name='Должности'),
        ),
        migrations.AddField(
            model_name='salon',
            name='service',
            field=models.ManyToManyField(blank=True, related_name='salon_staffers', to='services.Category', verbose_name='Категория услуг'),
        ),
        migrations.AddField(
            model_name='salon',
            name='staffers',
            field=models.ManyToManyField(blank=True, related_name='salon_staffers', to='staffer.Staffer', verbose_name='Сотрудники'),
        ),
    ]
