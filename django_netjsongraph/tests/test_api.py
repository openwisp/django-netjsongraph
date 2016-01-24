from django.test import TestCase
from ..models import Topology, Link, Node

from .utils import UnpublishMixin, LoadMixin


class TestRestFramework(TestCase, UnpublishMixin, LoadMixin):
    fixtures = [
        'test_topologies.json',
        'test_nodes.json'
    ]

    list_url = '/api/topology/'
    detail_url = '/api/topology/a083b494-8e16-4054-9537-fb9eba914861/'
    receive_url = '/api/receive/a083b494-8e16-4054-9537-fb9eba914861/?key=test'

    def _set_receive(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.strategy = 'receive'
        t.key = 'test'
        t.expiration_time = 0
        t.save()

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.data['type'], 'NetworkCollection')
        self.assertEqual(len(response.data['collection']), 1)

    def test_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['type'], 'NetworkGraph')

    def test_list_unpublished(self):
        self._unpublish()
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data['collection']), 0)

    def test_detail_unpublished(self):
        self._unpublish()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 404)

    def test_receive(self):
        self._set_receive()
        Node.objects.all().delete()
        data = self._load('static/netjson-1-link.json')
        response = self.client.post(self.receive_url,
                                    data,
                                    content_type='text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'data received successfully')
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)

    def test_receive_404(self):
        # topology is set to FETCH strategy
        response = self.client.post(self.receive_url, content_type='text/plain')
        self.assertEqual(response.status_code, 404)

    def test_receive_415(self):
        self._set_receive()
        data = self._load('static/netjson-1-link.json')
        response = self.client.post(self.receive_url,
                                    data,
                                    content_type='application/xml')
        self.assertEqual(response.status_code, 415)

    def test_receive_400_missing_key(self):
        self._set_receive()
        data = self._load('static/netjson-1-link.json')
        response = self.client.post(self.receive_url.replace('?key=test', ''),
                                    data,
                                    content_type='text/plain')
        self.assertEqual(response.status_code, 400)
        self.assertIn('missing required', response.data['detail'])

    def test_receive_400_unrecognized_format(self):
        self._set_receive()
        Node.objects.all().delete()
        data = 'WRONG'
        response = self.client.post(self.receive_url,
                                    data,
                                    content_type='text/plain')
        self.assertEqual(response.status_code, 400)
        self.assertIn('not recognized', response.data['detail'])

    def test_receive_403(self):
        self._set_receive()
        data = self._load('static/netjson-1-link.json')
        response = self.client.post(self.receive_url.replace('?key=test', '?key=wrong'),
                                    data,
                                    content_type='text/plain')
        self.assertEqual(response.status_code, 403)

    def test_receive_options(self):
        self._set_receive()
        response = self.client.options(self.receive_url)
        self.assertEqual(response.data['parses'], ['text/plain'])
