from django.test import TestCase

from netdiff import OlsrParser

from ..models import Topology


class TestTopology(TestCase):
    """
    tests for Topology model
    """
    fixtures = [
        'test_topologies.json',
        'test_nodes.json'
    ]

    def test_parser(self):
        t = Topology.objects.first()
        self.assertIs(t.parser_class, OlsrParser)
