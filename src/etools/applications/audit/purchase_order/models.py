from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from etools.applications.environment.notifications import send_notification_with_template
from etools.applications.firms.models import BaseFirm, BaseStaffMember
from etools.libraries.djangolib.utils import get_environment


class AuditorFirm(BaseFirm):
    unicef_users_allowed = models.BooleanField(default=False, editable=False, verbose_name=_('UNICEF users allowed'),
                                               help_text=_('Allow UNICEF users to join and act as auditors.'))


class AuditorStaffMember(BaseStaffMember):
    auditor_firm = models.ForeignKey(
        AuditorFirm, verbose_name=_('Auditor'), related_name='staff_members',
        on_delete=models.CASCADE,
    )
    hidden = models.BooleanField(verbose_name=_('Hidden'), default=False)

    def __str__(self):
        auditor_firm_name = ' ({})'.format(self.auditor_firm.name) if hasattr(self, 'auditor_firm') else ''
        return f'{self.get_full_name()} {auditor_firm_name} [{self.user.email}]'

    def send_user_appointed_email(self, engagement):
        context = {
            'environment': get_environment(),
            'engagement': engagement.get_mail_context(user=self.user),
            'staff_member': self.user.get_full_name(),
        }

        send_notification_with_template(
            recipients=[self.user.email],
            template_name='audit/engagement/submit_to_auditor',
            context=context,
        )


class PurchaseOrderManager(models.Manager):
    def get_by_natural_key(self, order_number):
        return self.get(order_number=order_number)


class PurchaseOrder(TimeStampedModel, models.Model):
    order_number = models.CharField(
        verbose_name=_('Purchase Order Number'),
        blank=True,
        null=True,
        unique=True,
        max_length=30
    )
    auditor_firm = models.ForeignKey(
        AuditorFirm, verbose_name=_('Auditor'), related_name='purchase_orders',
        on_delete=models.CASCADE,
    )
    contract_start_date = models.DateField(verbose_name=_('PO Date'), null=True, blank=True)
    contract_end_date = models.DateField(verbose_name=_('Contract Expiry Date'), null=True, blank=True)

    objects = PurchaseOrderManager()

    def __str__(self):
        return self.order_number

    def natural_key(self):
        return self.order_number,


class PurchaseOrderItemManager(models.Manager):
    def get_by_natural_key(self, purchase_order, number):
        return self.get(purchase_order=purchase_order, number=number)


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder, related_name='items', verbose_name=_('Purchase Order'),
        on_delete=models.CASCADE,
    )
    number = models.IntegerField(verbose_name=_('PO Item Number'))

    objects = PurchaseOrderItemManager()

    class Meta:
        unique_together = ('purchase_order', 'number')

    def natural_key(self):
        return self.purchase_order, self.number

    def __str__(self):
        return '{0.purchase_order}/{0.number}'.format(self)
