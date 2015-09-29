from django.test import TestCase

from ..models import Node


class TestNode(TestCase):
    """
    tests for Node model
    """
    def test_node_local_addresses_single(self):
        n = Node(label='test node')
        n.addresses = '192.168.0.1'
        n.full_clean()
        n.save()
        self.assertEqual(n.addresses, '192.168.0.1;')
        self.assertEqual(n.local_addresses, ['192.168.0.1'])

    def test_node_local_addresses_multiple(self):
        n = Node(label='test node')
        n.addresses = '192.168.0.1;  10.0.0.1,10.0.0.2'
        n.full_clean()
        n.save()
        self.assertEqual(n.addresses, '192.168.0.1; 10.0.0.1; 10.0.0.2;')
        self.assertEqual(n.local_addresses, ['192.168.0.1',
                                             '10.0.0.1',
                                             '10.0.0.2'])

    def test_node_name(self):
        n = Node(addresses='192.168.0.1,10.0.0.1')
        n._format_addresses()
        self.assertEqual(n.name, '192.168.0.1')
        n.label = 'test node'
        self.assertEqual(n.name, 'test node')
