from django.test import TestCase

from ..models import Topology


class TestRestFramework(TestCase):
    fixtures = [
        'test_topologies.json',
        'test_nodes.json'
    ]

    def test_list(self):
        response = self.client.get('/api/topology/')
        self.assertEqual(response.data['type'], 'NetworkCollection')
        self.assertEqual(len(response.data['collection']), 1)

    def test_detail(self):
        response = self.client.get('/api/topology/a083b494-8e16-4054-9537-fb9eba914861/')
        self.assertEqual(response.data['type'], 'NetworkGraph')
