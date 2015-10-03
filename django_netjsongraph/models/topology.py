import json
from collections import OrderedDict

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.module_loading import import_string
from django.utils.functional import cached_property

from netdiff import diff, NetJsonParser

from ..base import TimeStampedEditableModel
from ..settings import PARSERS


@python_2_unicode_compatible
class BaseTopology(TimeStampedEditableModel):
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

    @cached_property
    def parser_class(self):
        return import_string(self.parser)

    @property
    def latest(self):
        return self.parser_class(self.url, timeout=5)

    def diff(self):
        """ shortcut to netdiff.diff """
        latest = self.latest
        current = NetJsonParser(self.json(dict=True))
        return diff(current, latest)

    def json(self, dict=False, **kwargs):
        """ returns a dict that represents a NetJSON NetworkGraph object """
        nodes = []
        links = []
        # populate graph
        for link in self.link_set.select_related('source', 'target'):
            nodes.append(link.source.json(dict=True))
            nodes.append(link.target.json(dict=True))
            links.append(link.json(dict=True))
        netjson = OrderedDict((
            ('type', 'NetworkGraph'),
            ('protocol', self.parser_class.protocol),
            ('version', self.parser_class.version),
            ('metric', self.parser_class.metric),
            ('label', self.label),
            ('nodes', nodes),
            ('links', links)
        ))
        if dict:
            return netjson
        return json.dumps(netjson, **kwargs)

    def update(self):
        """
        Updates topology
        Links are not deleted straightaway but set as "down"
        """
        from . import Link, Node  # avoid circular dependency
        diff = self.diff()

        status = {
            'added': 'up',
            'removed': 'down',
            'changed': 'up'
        }
        from django.db.models import Q

        try:
            added_nodes = diff['added']['nodes']
        except TypeError:
            added_nodes = []

        #import pdb; pdb.set_trace()

        for node_dict in added_nodes:
            node = Node.objects.filter(addresses__contains=node_dict['id']).count()
            if node:
                continue
            addresses = '{0};'.format(node_dict['id'])
            addresses += ';'.join(node_dict.get('local_addresses', []))
            #label = node_dict.get('label', '')
            properties = node_dict.get('properties', {})
            node = Node(addresses=addresses,
                        properties=properties)
            node.full_clean()
            node.save()

        for section in ['added', 'removed', 'changed']:
            # if section is empty skip to next one
            if not diff[section]:
                continue
            for link_dict in diff[section]['links']:
                source_q = '{0};'.format(link_dict['source'])
                target_q = '{0};'.format(link_dict['target'])
                q = (Q(source__addresses__contains=source_q,
                       target__addresses__contains=target_q) |
                     Q(source__addresses__contains=target_q,
                       target__addresses__contains=source_q))
                link = Link.objects.filter(q).first()
                if not link:
                    source = Node.objects.filter(addresses__contains=source_q).first()
                    target = Node.objects.filter(addresses__contains=target_q).first()
                    link = Link(source=source,
                                target=target,
                                cost=link_dict['cost'],
                                properties=link_dict.get('properties', {}),
                                topology=self)
                try:
                    link.full_clean()
                except ValidationError as e:
                    msg = 'Exception while updating {0}'.format(self.__repr__())
                    #logger.exception(msg)
                    print('{0}\n{1}\n'.format(msg, e))
                    continue
                if section in ['changed', 'removed']:
                    link.status = status[section]
                    link.cost = link_dict['cost']
                    link.full_clean()
                link.save()
