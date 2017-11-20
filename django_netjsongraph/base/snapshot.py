from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import TimeStampedEditableModel

KINDS = (
    ('normal', _('NORMAL')),
    ('block_cut_tree', _('BLOCK_CUT_TREE'))
)


class AbstractSnapshot(TimeStampedEditableModel):
    """
    NetJSON NetworkGraph Snapshot implementation
    """
    topology = models.ForeignKey('django_netjsongraph.topology')
    data = models.TextField(blank=False)
    date = models.DateField(auto_now=True)
    kind = models.CharField(_('kind'),
                            max_length=16,
                            choices=KINDS,
                            default='normal',
                            db_index=True)

    class Meta:
        verbose_name_plural = _('snapshots')
        abstract = True

    def __str__(self):
        return "{0}: {1}".format(self.topology.label, self.date)
