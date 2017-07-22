from ..utils import LoadMixin, UnpublishMixin


class TestApiMixin(UnpublishMixin, LoadMixin):
    list_url = '/api/topology/'

    def detail_url(self):
        t = self.topology_model.objects.first()
        return '/api/topology/{0}/'.format(t.pk)

    def receive_url(self):
        t = self.topology_model.objects.first()
        return '/api/receive/{0}/?key=test'.format(t.pk)

    def _set_receive(self, topology_model):
        t = topology_model.objects.first()
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
        response = self.client.get(self.detail_url())
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
        self._set_receive(self.topology_model)
        self.node_model.objects.all().delete()
        data = self._load('static/netjson-1-link.json')
        response = self.client.post(self.receive_url(),
                                    data,
                                    content_type='text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'data received successfully')
        self.assertEqual(self.node_model.objects.count(), 2)
        self.assertEqual(self.link_model.objects.count(), 1)

    def test_receive_404(self):
        # topology is set to FETCH strategy
        response = self.client.post(self.receive_url(), content_type='text/plain')
        self.assertEqual(response.status_code, 404)

    def test_receive_415(self):
        self._set_receive(self.topology_model)
        data = self._load('static/netjson-1-link.json')
        response = self.client.post(self.receive_url(),
                                    data,
                                    content_type='application/xml')
        self.assertEqual(response.status_code, 415)

    def test_receive_400_missing_key(self):
        self._set_receive(self.topology_model)
        data = self._load('static/netjson-1-link.json')
        response = self.client.post(self.receive_url().replace('?key=test', ''),
                                    data,
                                    content_type='text/plain')
        self.assertEqual(response.status_code, 400)
        self.assertIn('missing required', response.data['detail'])

    def test_receive_400_unrecognized_format(self):
        self._set_receive(self.topology_model)
        self.node_model.objects.all().delete()
        data = 'WRONG'
        response = self.client.post(self.receive_url(),
                                    data,
                                    content_type='text/plain')
        self.assertEqual(response.status_code, 400)
        self.assertIn('not recognized', response.data['detail'])

    def test_receive_403(self):
        self._set_receive(self.topology_model)
        data = self._load('static/netjson-1-link.json')
        response = self.client.post(self.receive_url().replace('?key=test', '?key=wrong'),
                                    data,
                                    content_type='text/plain')
        self.assertEqual(response.status_code, 403)

    def test_receive_options(self):
        self._set_receive(self.topology_model)
        response = self.client.options(self.receive_url())
        self.assertEqual(response.data['parses'], ['text/plain'])
