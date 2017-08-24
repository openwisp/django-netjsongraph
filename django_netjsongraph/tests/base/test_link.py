import six
from django.core.exceptions import ValidationError

from ...utils import link_status_changed


class TestLinkMixin(object):
    def _get_nodes(self):
        return self.node_model.objects.all()

    def test_str(self):
        t = self.topology_model.objects.first()
        node1, node2 = self._get_nodes()
        l = t._create_link(source=node1, target=node2, cost=1.0)
        self.assertIsInstance(str(l), str)

    def test_clean_properties(self):
        t = self.topology_model.objects.first()
        node1, node2 = self._get_nodes()
        l = t._create_link(source=node1, target=node2, cost=1.0, properties=None)
        l.full_clean()
        self.assertEqual(l.properties, {})

    def test_same_source_and_target_id(self):
        t = self.topology_model.objects.first()
        node_id = self.node_model.objects.first().pk
        l = t._create_link(source_id=node_id, target_id=node_id, cost=1)
        with self.assertRaises(ValidationError):
            l.full_clean()

    def test_same_source_and_target(self):
        t = self.topology_model.objects.first()
        node = self.node_model.objects.first()
        l = t._create_link(source=node, target=node, cost=1)
        with self.assertRaises(ValidationError):
            l.full_clean()

    def test_json(self):
        t = self.topology_model.objects.first()
        node1, node2 = self._get_nodes()
        l = t._create_link(source=node1, target=node2, cost=1.0,
                           cost_text='100mbit/s', properties='{"pretty": true}')
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
        t = self.topology_model.objects.first()
        node1, node2 = self._get_nodes()
        l = t._create_link(source=node1, target=node2, cost=1.0,
                           cost_text='100mbit/s', properties='{"pretty": true}')
        l.full_clean()
        l.save()
        l = self.link_model.get_from_nodes('192.168.0.1', '192.168.0.2', t)
        self.assertIsInstance(l, self.link_model)
        l = self.link_model.get_from_nodes('wrong', 'wrong', t)
        self.assertIsNone(l)

    def test_status_change_signal_sent(self):
        self.signal_was_called = False
        t = self.topology_model.objects.first()
        node1, node2 = self._get_nodes()
        l = t._create_link(source=node1, target=node2, cost=1.0, status='up')
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
