from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel


class Category(OrderedModel, TimeStampedModel):
    MODULE_CHOICES = Choices(
        ('apd', _('Action Points')),
        ('t2f', _('Trip Management')),
        ('tpm', _('Third Party Monitoring')),
        ('audit', _('Financial Assurance')),
    )

    module = models.CharField(max_length=10, choices=MODULE_CHOICES, verbose_name=_('Module'))
    description = models.TextField(verbose_name=_('Description'))

    class Meta:
        unique_together = ("description", "module", )
        ordering = ('module', 'order')

    def __str__(self):
        return '{}: {}'.format(self.module, self.description)
