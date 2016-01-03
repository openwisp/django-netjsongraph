from django.test import TestCase

from .utils import UnpublishMixin


class TestVisualizer(TestCase, UnpublishMixin):
    fixtures = [
        'test_topologies.json',
        'test_nodes.json'
    ]

    def test_list(self):
        response = self.client.get('/')
        self.assertContains(response, 'TestNetwork')

    def test_detail(self):
        response = self.client.get('/topology/a083b494-8e16-4054-9537-fb9eba914861/')
        self.assertContains(response, 'a083b494-8e16-4054-9537-fb9eba914861')

    def test_list_unpublished(self):
        self._unpublish()
        response = self.client.get('/')
        self.assertNotContains(response, 'TestNetwork')

    def test_detail_unpublished(self):
        self._unpublish()
        response = self.client.get('/topology/a083b494-8e16-4054-9537-fb9eba914861/')
        self.assertEqual(response.status_code, 404)
