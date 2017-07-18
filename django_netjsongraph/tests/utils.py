import json
import logging
import os
import sys
from contextlib import contextmanager
from datetime import timedelta

import responses
from django.core.management import call_command
from django.test.runner import DiscoverRunner
from django.utils.timezone import now

from .. import settings

try:
    from cStringIO import StringIO  # noqa
except ImportError:
    from io import StringIO  # noqa


@contextmanager
def redirect_stdout(stream):
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = sys.__stdout__


class LoggingDisabledTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        # disable logging below CRITICAL while testing
        logging.disable(logging.CRITICAL)
        return super(LoggingDisabledTestRunner, self).run_tests(test_labels,
                                                                extra_tests,
                                                                **kwargs)


class UnpublishMixin(object):
    def _unpublish(self):
        t = self.topology_model.objects.first()
        t.published = False
        t.save()


class LoadMixin(object):
    def _load(self, file):
        d = os.path.dirname(os.path.abspath(__file__))
        return open(os.path.join(d, file)).read()


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


class TestUtilsMixin(LoadMixin):
    """
    tests for django_netjsongraph.utils
    """
    maxDiff = None

    @responses.activate
    def test_update_all_method(self):
        t = self.topology_model.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        self.node_model.objects.all().delete()
        self.topology_model.update_all('testnetwork')
        self.assertEqual(self.node_model.objects.count(), 2)
        self.assertEqual(self.link_model.objects.count(), 1)
        # test exception
        t.url = t.url.replace('9090', '9091')
        t.save()
        self.node_model.objects.all().delete()
        self.link_model.objects.all().delete()
        responses.add(responses.GET,
                      'http://127.0.0.1:9091',
                      body=self._load('static/netjson-invalid.json'),
                      content_type='application/json')
        # capture output
        output = StringIO()
        with redirect_stdout(output):
            self.topology_model.update_all()

        self.assertEqual(self.node_model.objects.count(), 1)
        self.assertEqual(self.link_model.objects.count(), 0)
        self.assertIn('Failed to', output.getvalue())

    @responses.activate
    def test_update_topology_command(self):
        t = self.topology_model.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        self.node_model.objects.all().delete()
        self.topology_model.update_all()
        self.assertEqual(self.node_model.objects.count(), 2)
        self.assertEqual(self.link_model.objects.count(), 1)
        # test exception
        t.url = t.url.replace('9090', '9091')
        t.save()
        self.node_model.objects.all().delete()
        self.link_model.objects.all().delete()
        responses.add(responses.GET,
                      'http://127.0.0.1:9091',
                      body=self._load('static/netjson-invalid.json'),
                      content_type='application/json')
        # capture output
        output = StringIO()
        with redirect_stdout(output):
            call_command('update_topology')

        self.assertEqual(self.node_model.objects.count(), 1)
        self.assertEqual(self.link_model.objects.count(), 0)
        self.assertIn('Failed to', output.getvalue())

    @responses.activate
    def test_update_all_method_unpublished(self):
        t = self.topology_model.objects.first()
        t.published = False
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        self.node_model.objects.all().delete()
        self.topology_model.update_all()
        self.assertEqual(self.node_model.objects.count(), 0)
        self.assertEqual(self.link_model.objects.count(), 0)

    @responses.activate
    def test_delete_expired_links(self):
        t = self.topology_model.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        # should not delete
        almost_expired_date = now() - timedelta(days=settings.LINK_EXPIRATION-10)
        n1 = self.node_model.objects.all()[0]
        n2 = self.node_model.objects.all()[1]
        l = self._create_link(source=n1,
                              target=n2,
                              cost=1,
                              status='down',
                              topology=t)
        self.link_model.objects.filter(pk=l.pk).update(created=almost_expired_date,
                                                       modified=almost_expired_date)
        empty_topology = json.dumps({
            "type": "NetworkGraph",
            "protocol": "OLSR",
            "version": "0.8",
            "metric": "ETX",
            "nodes": [],
            "links": []
        })
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=empty_topology,
                      content_type='application/json')
        self.topology_model.update_all('testnetwork')
        self.assertEqual(self.node_model.objects.count(), 2)
        self.assertEqual(self.link_model.objects.count(), 1)
        # should delete
        expired_date = now() - timedelta(days=settings.LINK_EXPIRATION+10)
        self.link_model.objects.filter(pk=l.pk).update(created=expired_date,
                                                       modified=expired_date)
        self.topology_model.update_all('testnetwork')
        self.assertEqual(self.node_model.objects.count(), 2)
        self.assertEqual(self.link_model.objects.count(), 0)

    @responses.activate
    def test_delete_expired_disabled(self):
        t = self.topology_model.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        n1 = self.node_model.objects.all()[0]
        n2 = self.node_model.objects.all()[1]
        l = self._create_link(source=n1,
                              target=n2,
                              cost=1,
                              status='down',
                              topology=t)
        expired_date = now() - timedelta(days=settings.LINK_EXPIRATION+10)
        self.link_model.objects.filter(pk=l.pk).update(created=expired_date,
                                                       modified=expired_date)
        empty_topology = json.dumps({
            "type": "NetworkGraph",
            "protocol": "OLSR",
            "version": "0.8",
            "metric": "ETX",
            "nodes": [],
            "links": []
        })
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=empty_topology,
                      content_type='application/json')
        ORIGINAL_LINK_EXPIRATION = int(settings.LINK_EXPIRATION)
        settings.LINK_EXPIRATION = False
        self.topology_model.update_all('testnetwork')
        self.assertEqual(self.node_model.objects.count(), 2)
        self.assertEqual(self.link_model.objects.count(), 1)
        settings.LINK_EXPIRATION = ORIGINAL_LINK_EXPIRATION
