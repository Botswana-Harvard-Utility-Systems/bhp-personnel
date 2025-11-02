from django.apps import AppConfig as DjangoAppConfig

from edc_base.apps import AppConfig as BaseEdcBaseAppConfig


class AppConfig(DjangoAppConfig):
    name = 'bhp_personnel'
    verbose_name = 'Contract Management'
    admin_site_name = 'bhp_personnel_admin'
    identifier_pattern = None

    def ready(self):
        import bhp_personnel.models.signals


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'Contract Management System'
    institution = 'Botswana-Harvard AIDS Institute'
