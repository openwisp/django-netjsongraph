import six
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Link, Node, Topology
from ..utils import link_status_changed


class TestLink(TestCase):
    """
    tests for Link model
    """
    fixtures = [
        'test_topologies.json',
        'test_nodes.json'
    ]

    def test_str(self):
        l = Link(topology_id="a083b494-8e16-4054-9537-fb9eba914861",
                 source_id="d083b494-8e16-4054-9537-fb9eba914861",
                 target_id="d083b494-8e16-4054-9537-fb9eba914862",
                 cost=1.0)
        self.assertIsInstance(str(l), str)

    def test_clean_properties(self):
        l = Link(topology_id="a083b494-8e16-4054-9537-fb9eba914861",
                 source_id="d083b494-8e16-4054-9537-fb9eba914861",
                 target_id="d083b494-8e16-4054-9537-fb9eba914862",
                 cost=1.0,
                 properties=None)
        l.full_clean()
        self.assertEqual(l.properties, {})

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

    def test_json(self):
        l = Link(topology_id="a083b494-8e16-4054-9537-fb9eba914861",
                 source_id="d083b494-8e16-4054-9537-fb9eba914861",
                 target_id="d083b494-8e16-4054-9537-fb9eba914862",
                 cost=1.0,
                 cost_text='100mbit/s',
                 properties='{"pretty": true}')
        self.assertEqual(dict(l.json(dict=True)), {
            'source': '192.168.0.1',
            'target': '192.168.0.2',
            'cost': 1.0,
            'cost_text': '100mbit/s',
            'properties': {
                'pretty': True,
                'status': 'up',
                'created': l.created,
                'modified': l.modified
            }
        })
        self.assertIsInstance(l.json(), six.string_types)

    def test_get_from_nodes(self):
        l = Link(topology_id="a083b494-8e16-4054-9537-fb9eba914861",
                 source_id="d083b494-8e16-4054-9537-fb9eba914861",
                 target_id="d083b494-8e16-4054-9537-fb9eba914862",
                 cost=1.0,
                 cost_text='100mbit/s',
                 properties='{"pretty": true}')
        l.full_clean()
        l.save()
        t = Topology.objects.get(pk='a083b494-8e16-4054-9537-fb9eba914861')
        l = Link.get_from_nodes('192.168.0.1', '192.168.0.2', t)
        self.assertIsInstance(l, Link)
        l = Link.get_from_nodes('wrong', 'wrong', t)
        self.assertIsNone(l)

    def test_status_change_signal_sent(self):
        self.signal_was_called = False
        l = Link(topology_id="a083b494-8e16-4054-9537-fb9eba914861",
                 source_id="d083b494-8e16-4054-9537-fb9eba914861",
                 target_id="d083b494-8e16-4054-9537-fb9eba914862",
                 cost=1.0,
                 status='up')
        l.save()

        def handler(sender, link, **kwargs):
            self.signal_was_called = True
            self.assertEqual(link.pk, l.pk)
            self.assertEqual(link.status, 'down')

        link_status_changed.connect(handler)
        l.status = 'down'
        l.save()

        self.assertTrue(self.signal_was_called)
        link_status_changed.disconnect(handler)
