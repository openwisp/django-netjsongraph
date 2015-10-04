import os
import sys
import six
import responses

from django.test import TestCase
from django.core.management import call_command
from netdiff import OlsrParser

from ..models import Topology, Link, Node
from ..utils import update_topology
from .utils import StringIO, redirect_stdout


class TestTopology(TestCase):
    """
    tests for Topology model
    """
    fixtures = [
        'test_topologies.json',
        'test_nodes.json'
    ]
    maxDiff = None

    def _get_nodes(self):
        return Node.objects.all()

    def _load(self, file):
        d = os.path.dirname(os.path.abspath(__file__))
        return open(os.path.join(d, file)).read()

    def test_parser(self):
        t = Topology.objects.first()
        self.assertIs(t.parser_class, OlsrParser)

    def test_json_empty(self):
        t = Topology.objects.first()
        graph = t.json(dict=True)
        self.assertDictEqual(graph, {
            'type': 'NetworkGraph',
            'protocol': 'OLSR',
            'version': '0.8',
            'metric': 'ETX',
            'label': t.label,
            'nodes': [],
            'links': []
        })

    def test_json(self):
        node1, node2 = self._get_nodes()
        t = Topology.objects.first()
        l = Link.objects.create(topology=t, source=node1,
                                target=node2, cost=1)
        graph = t.json(dict=True)
        self.assertDictEqual(dict(graph), {
            'type': 'NetworkGraph',
            'protocol': 'OLSR',
            'version': '0.8',
            'metric': 'ETX',
            'label': t.label,
            'nodes': [
                dict(node1.json(dict=True)),
                dict(node2.json(dict=True))
            ],
            'links': [
                dict(l.json(dict=True))
            ]
        })
        self.assertIsInstance(t.json(), six.string_types)

    @responses.activate
    def test_empty_diff(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=t.json(),
                      content_type='application/json')
        self.assertDictEqual(t.diff(), {
            'added': None,
            'removed': None,
            'changed': None
        })

    @responses.activate
    def test_update_added(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        Node.objects.all().delete()
        t.update()
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)
        node1 = Node.objects.get(addresses__contains='192.168.0.1;')
        node2 = Node.objects.get(addresses__contains='192.168.0.2;')
        self.assertEqual(node1.local_addresses, ['10.0.0.1'])
        self.assertEqual(node1.properties, {'gateway': True})
        link = Link.objects.first()
        self.assertIn(link.source, [node1, node2])
        self.assertIn(link.target, [node1, node2])
        self.assertEqual(link.cost, 1.0)
        self.assertEqual(link.properties, {'pretty': True})
        # ensure repeating the action is idempotent
        t.update()
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)

    @responses.activate
    def test_update_changed(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        Node.objects.all().delete()
        t.update()
        link = Link.objects.first()
        # now change
        t.url = t.url.replace('9090', '9091')
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9091',
                      body=self._load('static/netjson-2-links.json'),
                      content_type='application/json')
        t.update()
        link.refresh_from_db()
        self.assertEqual(Node.objects.count(), 3)
        self.assertEqual(Link.objects.count(), 2)
        self.assertEqual(link.cost, 1.5)

    @responses.activate
    def test_update_removed(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-2-links.json'),
                      content_type='application/json')
        Node.objects.all().delete()
        t.update()
        self.assertEqual(Node.objects.count(), 3)
        self.assertEqual(Link.objects.count(), 2)
        # now change
        t.url = t.url.replace('9090', '9091')
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9091',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        t.update()
        self.assertEqual(Node.objects.count(), 3)
        self.assertEqual(Link.objects.count(), 2)
        self.assertEqual(Link.objects.filter(status='down').count(), 1)
        link = Link.objects.filter(status='down').first()
        self.assertIn('192.168.0.3', [link.source.netjson_id,
                                      link.target.netjson_id])
        self.assertEqual(link.cost, 2.0)

    @responses.activate
    def test_update_topology_func(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        Node.objects.all().delete()
        update_topology('testnetwork')
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)
        # test exception
        t.url = t.url.replace('9090', '9091')
        t.save()
        Node.objects.all().delete()
        Link.objects.all().delete()
        responses.add(responses.GET,
                      'http://127.0.0.1:9091',
                      body=self._load('static/netjson-invalid.json'),
                      content_type='application/json')
        # capture output
        output = StringIO()
        with redirect_stdout(output):
            update_topology()

        self.assertEqual(Node.objects.count(), 1)
        self.assertEqual(Link.objects.count(), 0)
        self.assertIn('Failed to', output.getvalue())

    @responses.activate
    def test_update_topology_command(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        Node.objects.all().delete()
        update_topology()
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)
        # test exception
        t.url = t.url.replace('9090', '9091')
        t.save()
        Node.objects.all().delete()
        Link.objects.all().delete()
        responses.add(responses.GET,
                      'http://127.0.0.1:9091',
                      body=self._load('static/netjson-invalid.json'),
                      content_type='application/json')
        # capture output
        output = StringIO()
        with redirect_stdout(output):
            call_command('update_topology')

        self.assertEqual(Node.objects.count(), 1)
        self.assertEqual(Link.objects.count(), 0)
        self.assertIn('Failed to', output.getvalue())
