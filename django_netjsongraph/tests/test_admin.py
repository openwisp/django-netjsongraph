from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import Topology


class TestAdmin(TestCase):
    fixtures = [
        'test_topologies.json',
        'test_nodes.json',
        'test_users.json'
    ]

    def setUp(self):
        self.client.login(username='admin', password='tester')

    def test_unpublish_selected(self):
        path = reverse('admin:django_netjsongraph_topology_changelist')
        t = Topology.objects.first()
        self.assertEqual(t.published, True)
        response = self.client.post(path, {
            'action': 'unpublish_selected',
            '_selected_action': str(t.pk)
        })
        t.refresh_from_db()
        self.assertEqual(t.published, False)

    def test_publish_selected(self):
        path = reverse('admin:django_netjsongraph_topology_changelist')
        t = Topology.objects.first()
        t.published = False
        t.save()
        response = self.client.post(path, {
            'action': 'publish_selected',
            '_selected_action': str(t.pk)
        })
        t.refresh_from_db()
        self.assertEqual(t.published, True)
