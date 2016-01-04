import json
from collections import OrderedDict

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.module_loading import import_string
from django.utils.functional import cached_property

from rest_framework.utils.encoders import JSONEncoder
from netdiff import diff, NetJsonParser

from ..base import TimeStampedEditableModel
from ..settings import PARSERS, TIMEOUT
from ..contextmanagers import log_failure


@python_2_unicode_compatible
class BaseTopology(TimeStampedEditableModel):
    label = models.CharField(_('label'), max_length=64)
    parser = models.CharField(_('format'),
                              choices=PARSERS,
                              max_length=128,
                              help_text=_('Select topology format'))
    url = models.URLField(_('url'), help_text=_('Topology data will be fetched from this URL'))
    published = models.BooleanField(_('published'),
                                    default=True,
                                    help_text=_('Unpublished topologies won\'t be updated or'
                                                'shown in the visualizer'))

    # the following fields will be filled automatically
    protocol = models.CharField(_('protocol'), max_length=64, blank=True)
    version = models.CharField(_('version'), max_length=24, blank=True)
    revision = models.CharField(_('revision'), max_length=64, blank=True)
    metric = models.CharField(_('metric'), max_length=24, blank=True)

    class Meta:
        verbose_name_plural = _('topologies')
        abstract = True

    def __str__(self):
        return '{0} - {1}'.format(self.label, self.get_parser_display())

    def get_absolute_url(self):
        return reverse('topology_detail', args=[self.pk])

    @cached_property
    def parser_class(self):
        return import_string(self.parser)

    @property
    def latest(self):
        latest = self.parser_class(self.url, timeout=TIMEOUT)
        # update topology attributes if needed
        changed = False
        for attr in ['protocol', 'version', 'metric']:
            latest_attr = getattr(latest, attr)
            if getattr(self, attr) != latest_attr:
                setattr(self, attr, latest_attr)
                changed = True
        if changed:
            self.save()
        # return latest
        return latest

    def diff(self):
        """ shortcut to netdiff.diff """
        latest = self.latest
        current = NetJsonParser(self.json(dict=True, omit_down=True))
        return diff(current, latest)

    def json(self, dict=False, omit_down=False, **kwargs):
        """ returns a dict that represents a NetJSON NetworkGraph object """
        nodes = []
        links = []
        link_queryset = self.link_set.select_related('source', 'target')
        # needed to detect links coming back online
        if omit_down:
            link_queryset = link_queryset.filter(status='up')
        # populate graph
        for link in link_queryset:
            links.append(link.json(dict=True))
        for node in self.node_set.all():
            nodes.append(node.json(dict=True))
        netjson = OrderedDict((
            ('type', 'NetworkGraph'),
            ('protocol', self.protocol),
            ('version', self.version),
            ('metric', self.metric),
            ('label', self.label),
            ('id', str(self.id)),
            ('parser', self.parser),
            ('created', self.created),
            ('modified', self.modified),
            ('nodes', nodes),
            ('links', links)
        ))
        if dict:
            return netjson
        return json.dumps(netjson, cls=JSONEncoder, **kwargs)

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
                        properties=properties,
                        topology=self)
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
                if link.status != status[section]:
                    link.status = status[section]
                    changed = True
                if link.cost != link_dict['cost']:
                    link.cost = link_dict['cost']
                    changed = True
                # perform writes only if needed
                if changed:
                    with log_failure(action[section], link):
                        link.full_clean()
                        link.save()
