import six
from django.test import TestCase
from netdiff import OlsrParser

from ..models import Topology, Link, Node


class TestTopology(TestCase):
    """
    tests for Topology model
    """
    fixtures = [
        'test_topologies.json',
        'test_nodes.json'
    ]
    max_diff = None

    def _get_nodes(self):
        return Node.objects.all()

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
            'nodes': [
                dict(node1.json(dict=True)),
                dict(node2.json(dict=True))
            ],
            'links': [
                dict(l.json(dict=True))
            ]
        })
        self.assertIsInstance(t.json(), six.string_types)

