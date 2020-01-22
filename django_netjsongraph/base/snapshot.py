from django.db import models
from django.utils.translation import ugettext_lazy as _
from openwisp_utils.base import TimeStampedEditableModel


class AbstractSnapshot(TimeStampedEditableModel):
    """
    NetJSON NetworkGraph Snapshot implementation
    """
    topology = models.ForeignKey('django_netjsongraph.topology',
                                 on_delete=models.CASCADE)
    data = models.TextField(blank=False)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = _('snapshots')
        abstract = True

    def __str__(self):
        return "{0}: {1}".format(self.topology.label, self.date)
