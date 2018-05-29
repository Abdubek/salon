from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from salon.models import Salon

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Client(models.Model):
    UNKNOWN, MALE, WOMEN = 0, 1, 2
    GENDERS = (
        (UNKNOWN, _(u'Неизвестно')),
        (MALE, _(u'Мужской')),
        (WOMEN, _(u'Женский'))
    )

    full_name = models.CharField(
        max_length=255,
        verbose_name=_(u'Имя')
    )
    avatar = models.ImageField(
        upload_to='client',
        verbose_name=_(u'Аватар'),
        null=True,
        blank=True
    )
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 100)],
        format='JPEG'
    )
    phone = models.CharField(
        max_length=255,
        verbose_name=_(u'Сотовый')
    )
    email = models.CharField(
        max_length=255,
        verbose_name=_(u'Email'),
        null=True,
        blank=True
    )
    gender = models.PositiveSmallIntegerField(
        choices=GENDERS,
        default=UNKNOWN,
        verbose_name=_(u'Пол')
    )
    description = models.TextField(
        verbose_name=_(u'Комментарий'),
        null=True,
        blank=True
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse_lazy('client:detail', kwargs={'pk': self.pk})

    @property
    def avatar_url(self):
        img_url = "https://ui-avatars.com/api/?size=250&background=564FC1&color=fff&name=%s&font-size=0.4"

        if self.avatar:
            return self.avatar_thumbnail.url
        else:
            return img_url % self.full_name

    class Meta:
        verbose_name = _(u'Клиент')
        verbose_name_plural = _(u'Клиенты')
