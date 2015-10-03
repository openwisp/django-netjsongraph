from django.test import TestCase

from ..models import Node


class TestNode(TestCase):
    """
    tests for Node model
    """
    def test_node_address_list_single(self):
        n = Node(label='test node')
        n.addresses = '192.168.0.1'
        n.full_clean()
        n.save()
        self.assertEqual(n.addresses, '192.168.0.1;')
        self.assertEqual(n.address_list, ['192.168.0.1'])

    def test_node_address_list_semicolon(self):
        n = Node(label='test node')
        n.addresses = '192.168.0.1;'
        n.full_clean()
        n.save()
        self.assertEqual(n.addresses, '192.168.0.1;')
        self.assertEqual(n.address_list, ['192.168.0.1'])

    def test_node_address_list_multiple(self):
        n = Node(label='test node')
        n.addresses = '192.168.0.1;  10.0.0.1,10.0.0.2;10.0.0.3'
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
        n.addresses = '192.168.0.1;10.0.0.1;10.0.0.2;'
        self.assertEqual(n.local_addresses, ['10.0.0.1',
                                             '10.0.0.2'])

    def test_node_name(self):
        n = Node(addresses='192.168.0.1,10.0.0.1')
        n._format_addresses()
        self.assertEqual(n.name, '192.168.0.1')
        n.label = 'test node'
        self.assertEqual(n.name, 'test node')
