from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Link, Node, Topology


class TestLink(TestCase):
    """
    tests for Link model
    """
    fixtures = [
        'test_topologies.json',
        'test_nodes.json'
    ]

    def test_same_source_and_target_id(self):
        l = Link(topology_id="a083b494-8e16-4054-9537-fb9eba914861",
                 source_id="d083b494-8e16-4054-9537-fb9eba914861",
                 target_id="d083b494-8e16-4054-9537-fb9eba914861",
                 cost=1)
        with self.assertRaises(ValidationError):
            l.full_clean()

    def test_same_source_and_target(self):
        node = Node.objects.first()
        l = Link(topology=Topology.objects.first(),
                 source=node,
                 target=node,
                 cost=1)
        with self.assertRaises(ValidationError):
            l.full_clean()
