from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from salon.models import Salon
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='users',
        verbose_name=_(u'Аватар'),
        null=True,
        blank=True
    )
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 100)],
        format='JPEG'
    )
    about = models.TextField(
        verbose_name=_(u'Информация о себе'),
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        verbose_name=_(u'Номер мобильного'),
        max_length=20
    )
    manager = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    salon = models.ForeignKey(
        Salon,
        related_name='our_salon',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def get_absolute_url(self):
        return reverse_lazy('user:update', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def avatar_url(self):
        img_url = "https://ui-avatars.com/api/?size=250&background=564FC1&color=fff&name=%s&font-size=0.4"

        if self.avatar:
            return self.avatar_thumbnail.url
        else:
            return img_url % self.full_name
