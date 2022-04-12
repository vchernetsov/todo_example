from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from core.fields import UUIDPKField
from core.utils import tz_now

User = get_user_model()


class Task(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_FINISHED = 'finished'

    STATUS_CHOICES = {
        STATUS_PENDING: _('pending'),
        STATUS_FINISHED: _('finished'),
    }

    uuid = UUIDPKField()
    name = models.CharField(verbose_name=_('name'), max_length=100)
    description = models.TextField(verbose_name=_('description'), default='', blank=True)
    status = models.CharField(verbose_name=_('status'), max_length=20, choices=STATUS_CHOICES.items(),
                              default=STATUS_PENDING, db_index=True)

    created_at = models.DateTimeField(verbose_name=_('created at'), default=tz_now)
    owner = models.ForeignKey(User, verbose_name=_('owner'), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
