# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from services.models import Category
from staffer.models import Staffer, Position
from utils.models import CommonAbstractModel
from utils.cities import City

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Salon(CommonAbstractModel):
    CITIES = (
        (City.ASTANA.value, _(u'Астана')),
        (City.ALMATY.value, _(u'Aлматы')),
        (City.SEMEY.value, _(u'Семей'))
    )

    full_name = models.CharField(
        verbose_name=_(u'Название салона'),
        max_length=255
    )
    city = models.PositiveSmallIntegerField(
        default=City.ASTANA.value,
        choices=CITIES,
        verbose_name=_(u'Город')
    )
    logo = models.ImageField(
        upload_to='salon',
        verbose_name=_(u'Логотип'),
        null=True,
        blank=True
    )
    logo_thumbnail = ImageSpecField(
        source='logo',
        processors=[ResizeToFill(100, 100)],
        format='JPEG'
    )
    leader = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='owner',
        on_delete=models.CASCADE,
    )
    staffers = models.ManyToManyField(
        Staffer,
        blank=True,
        related_name='salon_staffers',
        verbose_name=_(u'Сотрудники')
    )
    positions = models.ManyToManyField(
        Position,
        blank=True,
        related_name='salon_staffers',
        verbose_name=_(u'Должности')
    )
    service_categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='service_category',
        verbose_name=_(u'Категории')
    )

    def get_absolute_url(self):
        return reverse_lazy('salon:detail', kwargs={'pk': self.pk})

    @property
    def avatar_url(self):
        img_url = "https://ui-avatars.com/api/?size=250&background=564FC1&color=fff&name=%s&font-size=0.4"

        if self.logo:
            return self.logo_thumbnail.url
        else:
            return img_url % self.full_name

    class Meta:
        verbose_name = _(u'Салон')
        verbose_name_plural = _(u'Салоны')


class Contact(CommonAbstractModel):
    salon = models.OneToOneField(
        Salon,
        on_delete=models.CASCADE
    )
    address = models.CharField(
        verbose_name=_(u'Адрес'),
        max_length=255,
        null=True,
        blank=True
    )
    zip_code = models.PositiveSmallIntegerField(
        verbose_name=_(u'Индекс'),
        null=True,
        blank=True
    )
    contact = models.CharField(
        verbose_name=_(u'Телефон'),
        max_length=20,
        null=True,
        blank=True
    )
    web_site = models.CharField(
        verbose_name=_(u'Сайт'),
        max_length=255,
        null=True,
        blank=True
    )
    timetable = models.CharField(
        verbose_name=_(u'График работы'),
        max_length=255,
        null=True,
        blank=True
    )

    def get_absolute_url(self):
        return reverse_lazy('salon:detail', kwargs={'pk': self.salon.pk})

    class Meta:
        verbose_name = _(u'Контакт')
        verbose_name_plural = _(u'Контакты')

