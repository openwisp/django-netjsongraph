from django.test import TestCase

from . import CreateGraphObjectsMixin
from ..models import Snapshot, Topology
from .base.test_snapshot import TestSnapshotMixin


class TestSnapshot(TestSnapshotMixin, CreateGraphObjectsMixin, TestCase):
    topology_model = Topology
    snapshot_model = Snapshot

    def setUp(self):
        self._create_topology().save_snapshot()
