from django.test import TestCase

from . import CreateGraphObjectsMixin
from ..models import Node, Topology
from .base.node import TestNodeMixin


class TestNode(TestNodeMixin, CreateGraphObjectsMixin, TestCase):
    topology_model = Topology
    node_model = Node
    maxDiff = 0

    def setUp(self):
        t = self._create_topology()
        self._create_node(label="node1", addresses="192.168.0.1;", topology=t)
        self._create_node(label="node2", addresses="192.168.0.2;", topology=t)
