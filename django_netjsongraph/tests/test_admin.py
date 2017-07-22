from django.test import TestCase

from . import CreateGraphObjectsMixin
from ..models import Link, Node, Topology
from .base.admin import TestAdminMixin


class TestAdmin(TestAdminMixin, TestCase, CreateGraphObjectsMixin):
    topology_model = Topology
    link_model = Link
    node_model = Node

    def setUp(self):
        t = self._create_topology()
        self._create_node(label="node1", addresses="192.168.0.1;", topology=t)
        self._create_node(label="node2", addresses="192.168.0.2;", topology=t)
        super(TestAdmin, self).setUp()
