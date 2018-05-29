from django.db import models


class CommonAbstractModel(models.Model):
    """
    Абстрактный класс, с двумя предопределенными полями
    1. Поле даты создания
    2. Поле даты модификации

    Оба поля заполняются автоматически и через админку не редактируются.
    """
    date_created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    date_changed = models.DateTimeField(auto_now=True, editable=False, verbose_name=u'Дата изменения')

    class Meta:
        abstract = True
