from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .settings import SIGNALS


class DjangoNetjsongraphConfig(AppConfig):
    name = 'django_netjsongraph'
    label = 'django_netjsongraph'
    verbose_name = _('Network Graph')

    def ready(self):
        if SIGNALS:  # pragma: nocover
            __import__(SIGNALS)
