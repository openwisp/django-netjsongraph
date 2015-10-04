import sys
import logging
logger = logging.getLogger(__name__)
from contextlib import contextmanager

from .models import Topology


def update_topology(label=None):
    """
    updates all the topology
    sends logs to the "nodeshot.networking" logger
    """
    if label:
        queryset = Topology.objects.filter(label__icontains=label)
    else:
        queryset = Topology.objects.all()
    for topology in queryset:
        # print info message if calling from management command
        if 'update_topology' in sys.argv:  # pragma no cover
            print('Updating topology {0}\n'.format(topology))
        with log_on_fail(topology, 'update'):
            topology.update()


@contextmanager
def log_on_fail(obj, method):
    try:
        yield
    except Exception as e:
        msg = 'Failed to call method "{0}" on {1}'.format(method,
                                                          obj.__repr__())
        logger.exception(msg)
        print('{0}: {1}\n see error log for more'
              'information\n'.format(msg, e.__class__))
