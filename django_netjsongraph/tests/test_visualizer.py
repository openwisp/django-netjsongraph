from django.test import TestCase


class TestVisualizer(TestCase):
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
