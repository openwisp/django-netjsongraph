import sys

from .contextmanagers import log_on_fail
from .models import Topology


def update_topology(label=None):
    """
    updates all the topology
    sends logs to the "nodeshot.networking" logger
    """
    queryset = Topology.objects.filter(published=True)
    if label:
        queryset = queryset.filter(label__icontains=label)
    for topology in queryset:
        # print info message if calling from management command
        if 'update_topology' in sys.argv:  # pragma no cover
            print('Updating topology {0}\n'.format(topology))
        with log_on_fail('update', topology):
            topology.update()
