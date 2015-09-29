from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from uuidfield import UUIDField

from ..base import TimeStampedEditableModel
from ..settings import PARSERS


@python_2_unicode_compatible
class BaseTopology(TimeStampedEditableModel):
    id = UUIDField(auto=True, primary_key=True)
    label = models.CharField(_('label'), max_length=64)
    parser = models.CharField(_('format'), choices=PARSERS,
                                           max_length=128,
                                           help_text=_('Select topology format'))
    url = models.URLField(_('url'), help_text=_('Topology data will be fetched from this URL'))

    # the following fields will be filled automatically
    protocol = models.CharField(_('protocol'), max_length=64, blank=True)
    version = models.CharField(_('version'), max_length=24, blank=True)
    revision = models.CharField(_('revision'), max_length=64, blank=True)
    metric = models.CharField(_('metric'), max_length=24, blank=True)

    class Meta:
        verbose_name_plural = _('topologies')
        abstract = True

    def __str__(self):
        return self.label
