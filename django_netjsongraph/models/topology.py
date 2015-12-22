import json
from collections import OrderedDict

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.module_loading import import_string
from django.utils.functional import cached_property

from netdiff import diff, NetJsonParser

from ..base import TimeStampedEditableModel
from ..settings import PARSERS
from ..contextmanagers import log_on_fail


@python_2_unicode_compatible
class BaseTopology(TimeStampedEditableModel):
    label = models.CharField(_('label'), max_length=64)
    parser = models.CharField(_('format'),
                              choices=PARSERS,
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
            source = link.source.json(dict=True)
            if source not in nodes:
                nodes.append(source)
            target = link.target.json(dict=True)
            if target not in nodes:
                nodes.append(target)
            links.append(link.json(dict=True))
        netjson = OrderedDict((
            ('type', 'NetworkGraph'),
            ('protocol', self.parser_class.protocol),
            ('version', self.parser_class.version),
            ('metric', self.parser_class.metric),
            ('label', self.label),
            ('id', str(self.id)),
            ('parser', self.parser),
            ('created', str(self.created)),
            ('modified', str(self.modified)),
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
        action = {
            'added': 'add',
            'changed': 'change',
            'removed': 'remove'
        }

        try:
            added_nodes = diff['added']['nodes']
        except TypeError:
            added_nodes = []

        for node_dict in added_nodes:
            node = Node.count_address(node_dict['id'])
            if node:  # pragma no cover
                continue
            addresses = '{0};'.format(node_dict['id'])
            addresses += ';'.join(node_dict.get('local_addresses', []))
            properties = node_dict.get('properties', {})
            node = Node(addresses=addresses,
                        properties=properties)
            node.full_clean()
            node.save()

        for section, graph in sorted(diff.items()):
            # if graph is empty skip to next one
            if not graph:
                continue
            for link_dict in graph['links']:
                changed = False
                link = Link.get_from_nodes(link_dict['source'],
                                           link_dict['target'])
                if not link:
                    source = Node.get_from_address(link_dict['source'])
                    target = Node.get_from_address(link_dict['target'])
                    link = Link(source=source,
                                target=target,
                                cost=link_dict['cost'],
                                properties=link_dict.get('properties', {}),
                                topology=self)
                    changed = True
                # links in changed and removed sections
                # are always changing therefore needs to be saved
                if section in ['changed', 'removed']:
                    link.status = status[section]
                    link.cost = link_dict['cost']
                    changed = True
                # perform writes only if needed
                if changed:
                    with log_on_fail(action[section], link):
                        link.full_clean()
                        link.save()
