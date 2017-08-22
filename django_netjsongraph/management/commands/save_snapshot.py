from . import BaseSaveSnapshotCommand
from ...models import Topology


class Command(BaseSaveSnapshotCommand):
    topology_model = Topology
