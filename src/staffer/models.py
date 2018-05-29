from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.db import models

from utils.models import CommonAbstractModel

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Position(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name=_(u'Название')
    )
    description = models.TextField(
        verbose_name=_(u'Описание')
    )

    @staticmethod
    def get_absolute_url():
        return reverse_lazy('staffer:position')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        verbose_name = _(u'Должность')
        verbose_name_plural = _(u'Должности')


class Staffer(CommonAbstractModel):
    MASTER_FIRED = (
        (True, _(u'Уволен')),
        (False, _(u'Работает'))
    )

    full_name = models.CharField(
        max_length=255,
        verbose_name=_(u'Имя')
    )
    avatar = models.ImageField(
        upload_to='staffer',
        verbose_name=_(u'Аватар'),
        null=True,
        blank=True
    )
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 100)],
        format='JPEG'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        verbose_name=_(u'Должность')
    )
    specialization = models.CharField(
        max_length=255,
        verbose_name=_(u'Специализация')
    )
    master_fired = models.BooleanField(
        choices=MASTER_FIRED,
        default=False,
        verbose_name=_(u'Статус')
    )
    description = models.TextField(
        verbose_name=_(u'Описание')
    )

    def get_absolute_url(self):
        return reverse_lazy('staffer:detail', kwargs={'pk': self.pk})

    @property
    def avatar_url(self):
        img_url = "https://ui-avatars.com/api/?size=250&background=564FC1&color=fff&name=%s&font-size=0.4"

        if self.avatar:
            return self.avatar_thumbnail.url
        else:
            return img_url % self.full_name

    class Meta:
        verbose_name = _(u'Сотрудник')
        verbose_name_plural = _(u' Сотрудники')


class StafferInfo(CommonAbstractModel):
    UNKNOWN, MEN, WOMAN = 0, 1, 2
    GENDERS = (
        (UNKNOWN, _(u'Неизвестно')),
        (MEN, _(u'Мужской')),
        (WOMAN, _(u'Женский'))
    )

    staffer = models.ForeignKey(
        Staffer,
        on_delete=models.CASCADE,
        verbose_name=_(u'Сотрудник')
    )
    date_of_employment = models.DateField(
        null=True,
        blank=True,
        verbose_name=_(u'Дата приема на работу')
    )
    phone_number = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        verbose_name=_(u'Номер телефона')
    )
    gender = models.PositiveSmallIntegerField(
        default=UNKNOWN,
        choices=GENDERS,
        verbose_name=_(u'Пол')
    )
    passport_data = models.TextField(
        null=True,
        blank=True,
        verbose_name=_(u'Паспортные данные')
    )
    iin = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_(u'ИИН')
    )

    class Meta:
        verbose_name = _(u'Дополнительная информация')
        verbose_name_plural = _(u'Дополнительные информации')
