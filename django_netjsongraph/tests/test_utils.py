import json
import responses
from datetime import timedelta

from django.test import TestCase, override_settings
from django.core.management import call_command
from django.utils.timezone import now

from ..models import Topology, Link, Node
from ..utils import update_topology
from .. import settings
from .utils import StringIO, LoadMixin, redirect_stdout


class TestUtils(TestCase, LoadMixin):
    """
    tests for django_netjsongraph.utils
    """
    fixtures = [
        'test_topologies.json',
        'test_nodes.json'
    ]
    maxDiff = None

    @responses.activate
    def test_update_topology_func(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        Node.objects.all().delete()
        update_topology('testnetwork')
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)
        # test exception
        t.url = t.url.replace('9090', '9091')
        t.save()
        Node.objects.all().delete()
        Link.objects.all().delete()
        responses.add(responses.GET,
                      'http://127.0.0.1:9091',
                      body=self._load('static/netjson-invalid.json'),
                      content_type='application/json')
        # capture output
        output = StringIO()
        with redirect_stdout(output):
            update_topology()

        self.assertEqual(Node.objects.count(), 1)
        self.assertEqual(Link.objects.count(), 0)
        self.assertIn('Failed to', output.getvalue())

    @responses.activate
    def test_update_topology_command(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        Node.objects.all().delete()
        update_topology()
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)
        # test exception
        t.url = t.url.replace('9090', '9091')
        t.save()
        Node.objects.all().delete()
        Link.objects.all().delete()
        responses.add(responses.GET,
                      'http://127.0.0.1:9091',
                      body=self._load('static/netjson-invalid.json'),
                      content_type='application/json')
        # capture output
        output = StringIO()
        with redirect_stdout(output):
            call_command('update_topology')

        self.assertEqual(Node.objects.count(), 1)
        self.assertEqual(Link.objects.count(), 0)
        self.assertIn('Failed to', output.getvalue())

    @responses.activate
    def test_update_topology_func_unpublished(self):
        t = Topology.objects.first()
        t.published = False
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        responses.add(responses.GET,
                      'http://127.0.0.1:9090',
                      body=self._load('static/netjson-1-link.json'),
                      content_type='application/json')
        Node.objects.all().delete()
        update_topology()
        self.assertEqual(Node.objects.count(), 0)
        self.assertEqual(Link.objects.count(), 0)

    @responses.activate
    def test_delete_expired_links(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        # should not delete
        almost_expired_date = now() - timedelta(days=settings.LINK_EXPIRATION-10)
        l = Link.objects.create(source_id='d083b494-8e16-4054-9537-fb9eba914861',
                                target_id='d083b494-8e16-4054-9537-fb9eba914862',
                                cost=1,
                                status='down',
                                topology=t)
        Link.objects.filter(pk=l.pk).update(created=almost_expired_date,
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
        update_topology('testnetwork')
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)
        # should delete
        expired_date = now() - timedelta(days=settings.LINK_EXPIRATION+10)
        Link.objects.filter(pk=l.pk).update(created=expired_date,
                                            modified=expired_date)
        update_topology('testnetwork')
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 0)

    @responses.activate
    def test_delete_expired_disabled(self):
        t = Topology.objects.first()
        t.parser = 'netdiff.NetJsonParser'
        t.save()
        l = Link.objects.create(source_id='d083b494-8e16-4054-9537-fb9eba914861',
                                target_id='d083b494-8e16-4054-9537-fb9eba914862',
                                cost=1,
                                status='down',
                                topology=t)
        expired_date = now() - timedelta(days=settings.LINK_EXPIRATION+10)
        Link.objects.filter(pk=l.pk).update(created=expired_date,
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
        update_topology('testnetwork')
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 1)
        settings.LINK_EXPIRATION = ORIGINAL_LINK_EXPIRATION
