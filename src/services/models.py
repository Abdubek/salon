# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from staffer.models import Staffer
from utils.models import CommonAbstractModel

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Category(CommonAbstractModel):
    GENERAL, MEN, WOMAN = 0, 1, 2
    GENDERS = (
        (GENERAL, _(u'Общие')),
        (MEN, _(u'Мужские')),
        (WOMAN, _(u'Женские'))
    )

    title_ru = models.CharField(
        max_length=255,
        verbose_name=_(u'Название категории RUS')
    )
    title_kz = models.CharField(
        max_length=255,
        verbose_name=_(u'Название категории KZ')
    )
    gender = models.PositiveSmallIntegerField(
        default=GENERAL,
        choices=GENDERS,
        verbose_name=_(u'Содержит услуги')
    )

    def __str__(self):
        return "%s/%s" % (self.title_kz, self.title_ru)

    class Meta:
        ordering = ['id']
        verbose_name = _(u'Категория')
        verbose_name_plural = _(u'Категории')


class Service(CommonAbstractModel):
    title_ru = models.CharField(
        max_length=255,
        verbose_name=_(u'Название услуги RUS')
    )
    title_kz = models.CharField(
        max_length=255,
        verbose_name=_(u'Название услуги KZ')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_(u'Категория')
    )
    image = models.ImageField(
        upload_to='services',
        verbose_name=_(u'Изображение'),
        null=True,
        blank=True
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(100, 100)],
        format='JPEG'
    )
    min_price = models.PositiveSmallIntegerField(
        verbose_name=_(u'Минимальная цена')
    )
    max_price = models.PositiveSmallIntegerField(
        verbose_name=_(u'Максимальная цена')
    )
    is_online = models.BooleanField(
        default=True,
        verbose_name=_(u'Онлайн-запись')
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='salon_manager',
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse_lazy('services:category-detail', kwargs={'pk': self.category.pk})

    @property
    def logo_url(self):
        img_url = "https://ui-avatars.com/api/?size=250&background=564FC1&color=fff&name=%s&font-size=0.4"

        if self.image:
            return self.image_thumbnail.url
        else:
            return img_url % self.title_kz

    class Meta:
        ordering = ['id']
        verbose_name = _(u'Услуга')
        verbose_name_plural = _(u'Услуги')


class ServiceMasters(CommonAbstractModel):
    master = models.ForeignKey(
        Staffer,
        on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name=_(u'Длительность услуги')
    )

    @property
    def duration_hours(self):
        hours = self.duration // 60
        return hours

    @property
    def duration_minutes(self):
        minutes = self.duration % 60
        return minutes

    class Meta:
        verbose_name = _(u'Услуга мастера')
        verbose_name_plural = _(u'Услуги мастеров')
