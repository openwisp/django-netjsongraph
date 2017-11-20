from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import TimeStampedEditableModel
from .topology import SNAPSHOT_KINDS


class AbstractSnapshot(TimeStampedEditableModel):
    """
    NetJSON NetworkGraph Snapshot implementation
    """
    topology = models.ForeignKey('django_netjsongraph.topology')
    data = models.TextField(blank=False)
    date = models.DateField(auto_now=True)
    kind = models.CharField(_('kind'),
                            max_length=16,
                            choices=SNAPSHOT_KINDS,
                            default=SNAPSHOT_KINDS[0],
                            db_index=True)

    class Meta:
        verbose_name_plural = _('snapshots')
        abstract = True

    def __str__(self):
        return "{0}: {1}".format(self.topology.label, self.date)
