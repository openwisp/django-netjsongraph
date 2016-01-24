import json
from collections import OrderedDict

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError

from rest_framework.utils.encoders import JSONEncoder
from jsonfield import JSONField
from model_utils.fields import StatusField
from model_utils import Choices

from ..base import TimeStampedEditableModel


@python_2_unicode_compatible
class BaseLink(TimeStampedEditableModel):
    """
    NetJSON NetworkGraph Link Object implementation
    """
    topology = models.ForeignKey('django_netjsongraph.Topology')
    source = models.ForeignKey('django_netjsongraph.Node',
                               related_name='source_node_set')
    target = models.ForeignKey('django_netjsongraph.Node',
                               related_name='target_node_set')
    cost = models.FloatField()
    cost_text = models.CharField(max_length=24, blank=True)
    STATUS = Choices('up', 'down')
    status = StatusField()
    properties = JSONField(default=dict,
                           blank=True,
                           load_kwargs={'object_pairs_hook': OrderedDict},
                           dump_kwargs={'indent': 4})

    class Meta:
        abstract = True

    def __str__(self):
        return '{0} - {1}'.format(self.source.name, self.target.name)

    def clean(self):
        if self.source == self.target or self.source_id == self.target_id:
            raise ValidationError(_('source and target must not be the same'))
        if self.properties is None:
            self.properties = {}

    def json(self, dict=False, **kwargs):
        """
        returns a NetJSON NetworkGraph Link object
        """
        netjson = OrderedDict((
            ('source', self.source.netjson_id),
            ('target', self.target.netjson_id),
            ('cost', self.cost),
        ))
        if self.cost_text:
            netjson['cost_text'] = self.cost_text
        # properties contain status by default
        properties = OrderedDict((
            ('status', self.status),
        ))
        if self.properties:
            properties.update(self.properties)
        netjson['properties'] = properties
        netjson['properties']['created'] = self.created
        netjson['properties']['modified'] = self.modified
        if dict:
            return netjson
        return json.dumps(netjson, cls=JSONEncoder, **kwargs)

    @classmethod
    def get_from_nodes(cls, source, target, topology):
        """
        Find link between source and target,
        (or vice versa, order is irrelevant).
        Source and target nodes must already exist.
        :param source: string
        :param target: string
        :param topology: Topology instance
        :returns: Link object or None
        """
        source = '{0};'.format(source)
        target = '{0};'.format(target)
        q = (Q(source__addresses__contains=source,
               target__addresses__contains=target) |
             Q(source__addresses__contains=target,
               target__addresses__contains=source))
        return cls.objects.filter(q).filter(topology=topology).first()
