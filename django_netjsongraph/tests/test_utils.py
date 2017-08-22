from django.test import TestCase

from . import CreateGraphObjectsMixin
from ..models import Link, Node, Snapshot, Topology
from .utils import TestUtilsMixin


class TestUtils(TestCase, TestUtilsMixin, CreateGraphObjectsMixin):
    topology_model = Topology
    node_model = Node
    link_model = Link
    snapshot_model = Snapshot

    def setUp(self):
        t1 = self._create_topology()
        self._create_node(label="node1", addresses="192.168.0.1;", topology=t1)
        self._create_node(label="node2", addresses="192.168.0.2;", topology=t1)
