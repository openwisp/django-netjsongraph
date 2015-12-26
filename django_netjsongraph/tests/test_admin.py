import responses

from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import Topology, Node, Link
from .utils import LoadMixin


class TestAdmin(TestCase, LoadMixin):
    fixtures = [
        'test_topologies.json',
        'test_nodes.json',
        'test_users.json'
    ]

    def setUp(self):
        self.client.login(username='admin', password='tester')
        self.changelist_path = reverse('admin:django_netjsongraph_topology_changelist')

    def test_unpublish_selected(self):
        t = Topology.objects.first()
        self.assertEqual(t.published, True)
        response = self.client.post(self.changelist_path, {
            'action': 'unpublish_selected',
            '_selected_action': str(t.pk)
        })
        t.refresh_from_db()
        self.assertEqual(t.published, False)

    def test_publish_selected(self):
        t = Topology.objects.first()
        t.published = False
        t.save()
        response = self.client.post(self.changelist_path, {
            'action': 'publish_selected',
            '_selected_action': str(t.pk)
        })
        t.refresh_from_db()
        self.assertEqual(t.published, True)

    @responses.activate
    def test_update_selected(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        Node.objects.all().delete()
        response = self.client.post(self.changelist_path, {
            'action': 'update_selected',
            '_selected_action': str(t.pk)
        })
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)
