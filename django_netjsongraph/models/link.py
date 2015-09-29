from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError

from uuidfield import UUIDField
from jsonfield import JSONField

from ..base import TimeStampedEditableModel


@python_2_unicode_compatible
class BaseLink(TimeStampedEditableModel):
    """
    NetJSON NetworkGraph Link Object implementation
    """
    id = UUIDField(auto=True, primary_key=True)
    topology = models.ForeignKey('netjsongraph.Topology')
    source = models.ForeignKey('netjsongraph.Node',
                               related_name='source_node_set')
    target = models.ForeignKey('netjsongraph.Node',
                               related_name='target_node_set')
    cost = models.FloatField()
    cost_text = models.CharField(max_length=24, blank=True)
    properties = JSONField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{0} - {1}'.format(self.source.name, self.target.name)

    def clean(self):
        if self.source is self.target or self.source_id is self.target_id:
            raise ValidationError(_('source and target must not be the same'))
