from django.db import models
from django.utils.translation import gettext as _

from client.models import Client
from salon.models import Salon
from services.models import ServiceMasters
from users.models import User
from utils.models import CommonAbstractModel


class TimeTable(CommonAbstractModel):
    ONLINE, OFFLINE = True, False
    TYPES = (
        (ONLINE, _(u"Онлайн")),
        (OFFLINE, _(u"Оффлайн"))
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE,
        verbose_name=_(u'Клиент')
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name=_(u'Клиент')
    )
    service_master = models.ForeignKey(
        ServiceMasters,
        on_delete=models.CASCADE,
        verbose_name=_(u'Услуга мастера')
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_(u'Менеджер')
    )
    start = models.DateTimeField(
        verbose_name=_(u'Начало сеанса')
    )
    end = models.DateTimeField(
        verbose_name=_(u'Завершение сеанса')
    )
    comment = models.TextField(
        verbose_name=_(u'Комментарии'),
        null=True,
        blank=True
    )
    amount = models.PositiveIntegerField(
        verbose_name=_(u'Сумма')
    )
    is_online = models.BooleanField(
        choices=TYPES,
        default=OFFLINE
    )
    device_uid = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        db_index=True
    )
