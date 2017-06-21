import six
from django.test import TestCase

from ..models import Node, Topology


class TestNode(TestCase):
    """
    tests for Node model
    """
    fixtures = ['test_topologies.json']
    maxDiff = 0

    def test_str(self):
        n = Node(addresses='192.168.0.1', label='test node')
        self.assertIsInstance(str(n), str)

    def test_clean_properties(self):
        t = Topology.objects.first()
        n = Node(addresses='192.168.0.1',
                 label='test node',
                 properties=None,
                 topology=t)
        n.full_clean()
        self.assertEqual(n.properties, {})

    def test_node_address_list_single(self):
        n = Node(label='test node',
                 addresses='192.168.0.1',
                 topology=Topology.objects.first())
        n.full_clean()
        n.save()
        self.assertEqual(n.addresses, '192.168.0.1;')
        self.assertEqual(n.address_list, ['192.168.0.1'])

    def test_node_address_list_semicolon(self):
        n = Node(label='test node',
                 addresses='192.168.0.1;',
                 topology=Topology.objects.first())
        n.full_clean()
        n.save()
        self.assertEqual(n.addresses, '192.168.0.1;')
        self.assertEqual(n.address_list, ['192.168.0.1'])

    def test_node_address_list_multiple(self):
        n = Node(label='test node',
                 addresses='192.168.0.1;  10.0.0.1,10.0.0.2;10.0.0.3',
                 topology=Topology.objects.first())
        n.full_clean()
        n.save()
        self.assertEqual(n.addresses, '192.168.0.1; 10.0.0.1; '
                                      '10.0.0.2; 10.0.0.3;')
        self.assertEqual(n.address_list, ['192.168.0.1',
                                          '10.0.0.1',
                                          '10.0.0.2',
                                          '10.0.0.3'])

    def test_node_local_addresses(self):
        n = Node(label='test node')
        n = Node(label='test node',
                 addresses='192.168.0.1;10.0.0.1;10.0.0.2;',
                 topology=Topology.objects.first())
        self.assertEqual(n.local_addresses, ['10.0.0.1',
                                             '10.0.0.2'])

    def test_node_name(self):
        n = Node(addresses='192.168.0.1,10.0.0.1')
        n._format_addresses()
        self.assertEqual(n.name, '192.168.0.1')
        n.label = 'test node'
        self.assertEqual(n.name, 'test node')

    def test_json(self):
        n = Node(label='test node',
                 addresses='192.168.0.1;10.0.0.1;',
                 properties='{"gateway": true}',
                 topology=Topology.objects.first())
        self.assertEqual(dict(n.json(dict=True)), {
            'id': '192.168.0.1',
            'label': 'test node',
            'local_addresses': ['10.0.0.1'],
            'properties': {
                'gateway': True,
                'created': n.created,
                'modified': n.modified
            }
        })
        self.assertIsInstance(n.json(), six.string_types)

    def test_get_from_address(self):
        t = Topology.objects.first()
        Node.objects.create(addresses='192.168.0.1,10.0.0.1',
                            topology=t)
        self.assertIsInstance(Node.get_from_address('192.168.0.1', t), Node)
        self.assertIsInstance(Node.get_from_address('10.0.0.1', t), Node)
        self.assertIsNone(Node.get_from_address('wrong', t))

    def test_count_address(self):
        t = Topology.objects.first()
        Node.objects.create(addresses='192.168.0.1,10.0.0.1',
                            topology=t)
        self.assertEqual(Node.count_address('192.168.0.1', t), 1)
        self.assertEqual(Node.count_address('0.0.0.0', t), 0)
