import six
import responses
from time import sleep

from django.test import TestCase
from django.core.exceptions import ValidationError
from netdiff import OlsrParser

from ..models import Topology, Link, Node
from .utils import LoadMixin


class TestTopology(TestCase, LoadMixin):
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

    def _set_receive(self, expiration_time=0):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.strategy = 'receive'
        t.key = 'test'
        t.expiration_time = expiration_time
        t.save()
        return t

    def test_str(self):
        t = Topology.objects.first()
        self.assertIsInstance(str(t), str)

    def test_parser(self):
        t = Topology.objects.first()
        self.assertIs(t.parser_class, OlsrParser)

    def test_json_empty(self):
        t = Topology.objects.first()
        Node.objects.all().delete()
        graph = t.json(dict=True)
        self.assertDictEqual(graph, {
            'type': 'NetworkGraph',
            'protocol': 'OLSR',
            'version': '0.8',
            'metric': 'ETX',
            'label': t.label,
            'id': str(t.id),
            'parser': t.parser,
            'created': t.created,
            'modified': t.modified,
            'nodes': [],
            'links': []
        })

    def test_json(self):
        node1, node2 = self._get_nodes()
        t = Topology.objects.first()
        node3 = Node.objects.create(topology=t, addresses='192.168.0.3', label='node3')
        l = Link.objects.create(topology=t, source=node1,
                                target=node2, cost=1)
        l2 = Link.objects.create(topology=t, source=node1,
                                 target=node3, cost=1)
        graph = t.json(dict=True)
        self.assertDictEqual(dict(graph), {
            'type': 'NetworkGraph',
            'protocol': 'OLSR',
            'version': '0.8',
            'metric': 'ETX',
            'label': t.label,
            'id': str(t.id),
            'parser': t.parser,
            'created': t.created,
            'modified': t.modified,
            'nodes': [
                dict(node1.json(dict=True)),
                dict(node2.json(dict=True)),
                dict(node3.json(dict=True))
            ],
            'links': [
                dict(l.json(dict=True)),
                dict(l2.json(dict=True))
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
    def test_update_topology_attributes(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        t.protocol = None
        t.version = None
        t.metric = None
        t.update()
        t.refresh_from_db()
        self.assertEqual(t.protocol, 'OLSR')
        self.assertEqual(t.version, '0.8')
        self.assertEqual(t.metric, 'ETX')

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
    def test_update_status_existing_link(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        l = Link(source_id='d083b494-8e16-4054-9537-fb9eba914861',
                 target_id='d083b494-8e16-4054-9537-fb9eba914862',
                 cost=1,
                 status='down',
                 properties={'pretty': True},
                 topology=t)
        l.full_clean()
        l.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        t.update()
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)
        l.refresh_from_db()
        self.assertEqual(l.status, 'up')

    def test_topology_url_empty(self):
        t = Topology(label='test',
                     parser='netdiff.NetJsonParser',
                     strategy='fetch')
        with self.assertRaises(ValidationError):
            t.full_clean()

    def test_topology_key_empty(self):
        t = Topology(label='test',
                     parser='netdiff.NetJsonParser',
                     strategy='receive',
                     key='')
        with self.assertRaises(ValidationError):
            t.full_clean()

    def _test_receive_added(self, expiration_time=0):
        Node.objects.all().delete()
        t = self._set_receive(expiration_time)
        data = self._load('static/netjson-1-link.json')
        t.receive(data)
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
        t.receive(data)
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)

    def test_receive_added(self):
        self._test_receive_added()

    def _test_receive_changed(self, expiration_time=0):
        t = self._set_receive(expiration_time)
        Node.objects.all().delete()
        data = self._load('static/netjson-1-link.json')
        t.receive(data)
        link = Link.objects.first()
        # now change
        data = self._load('static/netjson-2-links.json')
        t.receive(data)
        link.refresh_from_db()
        self.assertEqual(Node.objects.count(), 3)
        self.assertEqual(Link.objects.count(), 2)
        self.assertEqual(link.cost, 1.5)

    def test_receive_changed(self):
        self._test_receive_changed()

    def test_receive_removed(self):
        t = self._set_receive()
        Node.objects.all().delete()
        data = self._load('static/netjson-2-links.json')
        t.receive(data)
        self.assertEqual(Node.objects.count(), 3)
        self.assertEqual(Link.objects.count(), 2)
        # now change
        data = self._load('static/netjson-1-link.json')
        t.receive(data)
        self.assertEqual(Node.objects.count(), 3)
        self.assertEqual(Link.objects.count(), 2)
        self.assertEqual(Link.objects.filter(status='down').count(), 1)
        link = Link.objects.filter(status='down').first()
        self.assertIn('192.168.0.3', [link.source.netjson_id,
                                      link.target.netjson_id])
        self.assertEqual(link.cost, 2.0)

    def test_receive_status_existing_link(self):
        t = self._set_receive()
        l = Link(source_id='d083b494-8e16-4054-9537-fb9eba914861',
                 target_id='d083b494-8e16-4054-9537-fb9eba914862',
                 cost=1,
                 status='down',
                 properties={'pretty': True},
                 topology=t)
        l.full_clean()
        l.save()
        data = self._load('static/netjson-1-link.json')
        t.receive(data)
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)
        l.refresh_from_db()
        self.assertEqual(l.status, 'up')

    def test_multiple_receive_added(self):
        self._test_receive_added(expiration_time=50)

    def test_multiple_receive_changed(self):
        self._test_receive_changed(expiration_time=50)

    def test_multiple_receive_removed(self):
        t = self._set_receive(expiration_time=0.1)
        data = self._load('static/netjson-2-links.json')
        for sleep_time in [0, 0.2, 0.1]:
            sleep(sleep_time)
            t.receive(data)
            self.assertEqual(Node.objects.count(), 3)
            self.assertEqual(Link.objects.count(), 2)
            self.assertEqual(Link.objects.filter(status='down').count(), 0)
        # receive change
        data = self._load('static/netjson-1-link.json')
        t.receive(data)
        self.assertEqual(Node.objects.count(), 3)
        self.assertEqual(Link.objects.count(), 2)
        # expiration_time has not expired
        self.assertEqual(Link.objects.filter(status='down').count(), 0)
        # expiration_time has now expired for 1 link
        sleep(0.2)
        t.receive(data)
        self.assertEqual(Link.objects.filter(status='down').count(), 1)
        link = Link.objects.filter(status='down').first()
        self.assertIn('192.168.0.3', [link.source.netjson_id,
                                      link.target.netjson_id])
        self.assertEqual(link.cost, 2.0)

    def test_multiple_receive_split_network(self):
        def _assert_split_topology(self, topology):
            self.assertEqual(Node.objects.count(), 4)
            self.assertEqual(Link.objects.filter(status='up').count(), 2)
            self.assertEqual(Link.objects.filter(status='down').count(), 0)
            link = Link.get_from_nodes('192.168.0.1', '192.168.0.2', topology)
            self.assertIsNotNone(link)
            self.assertEqual(link.status, 'up')
            self.assertEqual(link.cost, 1.0)
            link = Link.get_from_nodes('192.168.0.10', '192.168.0.20', topology)
            self.assertIsNotNone(link)
            self.assertEqual(link.status, 'up')
            self.assertEqual(link.cost, 1.1)
        Node.objects.all().delete()
        t = self._set_receive(expiration_time=0.5)
        network1 = self._load('static/netjson-1-link.json')
        network2 = self._load('static/split-network.json')
        t.receive(network1)
        t.receive(network2)
        _assert_split_topology(self, t)
        for sleep_time in [0.1, 0.25, 0.3]:
            sleep(sleep_time)
            t.receive(network1)
            _assert_split_topology(self, t)
            sleep(sleep_time)
            t.receive(network2)
            _assert_split_topology(self, t)

    def test_very_long_addresses(self):
        """
        see https://github.com/interop-dev/django-netjsongraph/issues/6
        """
        t = self._set_receive()
        data = self._load('static/very-long-addresses.json')
        t.receive(data)
        n = Node.get_from_address('2001:4e12:452a:1:172::10', t)
        self.assertEqual(len(n.addresses), 485)
