from . import BaseUpdateCommand
from ...models import Topology


class Command(BaseUpdateCommand):
    topology_model = Topology
