# Generated by Django 2.0.4 on 2018-04-23 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staffer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_changed', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('title_ru', models.CharField(max_length=255, verbose_name='Название категории RUS')),
                ('title_kz', models.CharField(max_length=255, verbose_name='Название категории KZ')),
                ('gender', models.PositiveSmallIntegerField(choices=[(0, 'Общие'), (1, 'Мужские'), (2, 'Женские')], default=0, verbose_name='Содержит услуги')),
            ],
            options={
                'verbose_name_plural': 'Категории',
                'verbose_name': 'Категория',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_changed', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('title_ru', models.CharField(max_length=255, verbose_name='Название услуги RUS')),
                ('title_kz', models.CharField(max_length=255, verbose_name='Название услуги KZ')),
                ('image', models.ImageField(blank=True, null=True, upload_to='services', verbose_name='Изображение')),
                ('min_price', models.PositiveSmallIntegerField(verbose_name='Минимальная цена')),
                ('max_price', models.PositiveSmallIntegerField(verbose_name='Максимальная цена')),
                ('is_online', models.BooleanField(default=True, verbose_name='Онлайн-запись')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.Category', verbose_name='Категория')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salon_manager', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Услуги',
                'verbose_name': 'Услуга',
            },
        ),
        migrations.CreateModel(
            name='ServiceMasters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_changed', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('duration', models.PositiveSmallIntegerField(verbose_name='Длительность услуги')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staffer.Staffer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.Service')),
            ],
            options={
                'verbose_name_plural': 'Услуги мастеров',
                'verbose_name': 'Услуга мастера',
            },
        ),
    ]