import logging
logger = logging.getLogger(__name__)

from .models import Topology


def update_topology():
    """
    updates all the topology
    sends logs to the "nodeshot.networking" logger
    """
    for topology in Topology.objects.all():
        try:
            topology.update()
        except Exception as e:
            msg = 'Failed to update {}'.format(topology.__repr__())
            logger.exception(msg)
            print('{0}: {1}\n'
                  'see error log for more information\n'.format(msg, e.__class__))
