import logging
logger = logging.getLogger(__name__)
from contextlib import contextmanager

from .models import Topology


def update_topology():
    """
    updates all the topology
    sends logs to the "nodeshot.networking" logger
    """
    for topology in Topology.objects.all():
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
