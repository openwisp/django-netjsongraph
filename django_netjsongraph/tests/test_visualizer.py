from django.test import TestCase

from ..models import Node, Snapshot, Topology
from . import CreateGraphObjectsMixin
from .base.test_visualizer import TestVisualizerMixin


class TestVisualizer(TestVisualizerMixin, CreateGraphObjectsMixin, TestCase):
    topology_model = Topology
    node_model = Node
    snapshot_model = Snapshot

    def setUp(self):
        t = self._create_topology()
        self._create_node(label="node1", addresses=["192.168.0.1"], topology=t)
        self._create_node(label="node2", addresses=["192.168.0.2"], topology=t)
