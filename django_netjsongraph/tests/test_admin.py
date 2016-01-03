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
        self.client.post(self.changelist_path, {
            'action': 'unpublish_selected',
            '_selected_action': str(t.pk)
        })
        t.refresh_from_db()
        self.assertEqual(t.published, False)

    def test_publish_selected(self):
        t = Topology.objects.first()
        t.published = False
        t.save()
        self.client.post(self.changelist_path, {
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
        self.client.post(self.changelist_path, {
            'action': 'update_selected',
            '_selected_action': str(t.pk)
        })
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)

    @responses.activate
    def test_update_selected_failed(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body='{"error": "not found"}',
                      status=404,
                      content_type='application/json')
        Node.objects.all().delete()
        response = self.client.post(self.changelist_path, {
            'action': 'update_selected',
            '_selected_action': str(t.pk)
        }, follow=True)
        self.assertEqual(Node.objects.count(), 0)
        self.assertEqual(Link.objects.count(), 0)
        message = list(response.context['messages'])[0]
        self.assertEqual(message.tags, 'error')
        self.assertIn('not updated', message.message)

    def test_topology_viewonsite(self):
        t = Topology.objects.first()
        path = reverse('admin:django_netjsongraph_topology_change', args=[t.pk])
        response = self.client.get(path)
        self.assertContains(response, 'View on site')
        self.assertContains(response, t.get_absolute_url())

    def test_node_change_form(self):
        n = Node.objects.first()
        path = reverse('admin:django_netjsongraph_node_change', args=[n.pk])
        response = self.client.get(path)
        self.assertContains(response, 'Links to other nodes')

    def test_node_add(self):
        path = reverse('admin:django_netjsongraph_node_add')
        response = self.client.get(path)
        self.assertNotContains(response, 'Links to other nodes')
