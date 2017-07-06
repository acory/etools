from __future__ import unicode_literals

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = __name__.rpartition('.')[0]
    verbose_name = 'Auditor Portal'

    def ready(self):
        from . import signals
        from utils.permissions import signals
        signals.prepare_permission_choices(self.get_models())
