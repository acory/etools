from django.contrib.gis.db.models import PointField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import AutoSlugField
from model_utils.models import TimeStampedModel

from unicef_locations.models import Location

from etools.applications.field_monitoring.shared.models import Method
from etools.applications.reports.models import ResultType
from etools.applications.utils.groups.wrappers import GroupWrapper


class MethodType(models.Model):
    method = models.ForeignKey(Method, verbose_name=_('Method'))
    name = models.CharField(verbose_name=_('Name'), max_length=300)
    slug = AutoSlugField(verbose_name=_('Slug'), populate_from='name')

    def __str__(self):
        return self.name

    @staticmethod
    def clean_method(method):
        if not method.is_types_applicable:
            raise ValidationError(_('Unable to add type for this Method'))

    def clean(self):
        super().clean()
        self.clean_method(self.method)


class LocationSite(TimeStampedModel, models.Model):
    parent = models.ForeignKey(
        Location,
        verbose_name=_("Parent Location"),
        related_name='sites',
        db_index=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name=_("Name"), max_length=254)
    p_code = models.CharField(
        verbose_name=_("P Code"),
        max_length=32,
        blank=True,
        default='',
    )

    point = PointField(verbose_name=_("Point"), null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True, blank=True)

    security_detail = models.TextField(verbose_name=_('Detail on Security'), blank=True)

    @staticmethod
    def get_parent_location(point):
        matched_locations = Location.objects.filter(geom__contains=point)
        if not matched_locations:
            location = Location.objects.filter(gateway__admin_level=0).first()
        else:
            leafs = filter(lambda l: l.is_leaf_node(), matched_locations)
            location = min(leafs, key=lambda l: l.geom.length)

        return location

    def save(self, **kwargs):
        if not self.parent_id:
            self.parent = self.get_parent_location(self.point)
            assert self.parent_id, 'Unable to find location for {}'.format(self.point)

        super().save(**kwargs)


class CPOutputConfig(TimeStampedModel, models.Model):
    cp_output = models.OneToOneField('reports.Result', related_name='fm_config',
                                     verbose_name=_('CP Output To Be Monitored'))
    is_monitored = models.BooleanField(default=True, verbose_name=_('Monitored At Community Level?'))
    is_priority = models.BooleanField(verbose_name=_('Priority?'), default=False)
    government_partners = models.ManyToManyField('partners.PartnerOrganization', blank=True,
                                                 verbose_name=_('Contributing Government Partners'))

    def __str__(self):
        return self.cp_output.output_name

    @staticmethod
    def clean_cp_ouput(cp_otput):
        if cp_otput.result_type.name != ResultType.OUTPUT:
            raise ValidationError(_('Incorrect CP Output provided.'))

    def clean(self):
        super().clean()
        self.clean_cp_ouput(self.cp_output)


UNICEFUser = GroupWrapper(code='unicef_user',
                          name='UNICEF User')
