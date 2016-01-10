import sys

from datetime import timedelta
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.http import Http404

from .contextmanagers import log_failure
from .models import Topology, Link
from . import settings


def print_info(message):  # pragma no cover
    """
    print info message if calling from management command ``update_topology``
    """
    if 'update_topology' in sys.argv:
        print('{0}\n'.format(message))


def delete_expired_links():
    """
    deletes links that have been down for more than
    ``NETJSONGRAPH_LINK_EXPIRATION`` days
    """
    LINK_EXPIRATION = settings.LINK_EXPIRATION
    if LINK_EXPIRATION not in [False, None]:
        expiration_date = now() - timedelta(days=int(LINK_EXPIRATION))
        expired_links = Link.objects.filter(status='down',
                                            modified__lt=expiration_date)
        expired_links_length = len(expired_links)
        if expired_links_length:
            print_info('Deleting {0} expired links'.format(expired_links_length))
            for link in expired_links:
                link.delete()


def update_topology(label=None):
    """
    - updates topologies
    - logs failures
    - calls delete_expired_links()
    """
    queryset = Topology.objects.filter(published=True, strategy='fetch')
    if label:
        queryset = queryset.filter(label__icontains=label)
    for topology in queryset:
        print_info('Updating topology {0}'.format(topology))
        with log_failure('update', topology):
            topology.update()
    delete_expired_links()


def get_topology_or_404(pk, **kwargs):
    """
    retrieves topology with specified arguments or raises 404
    """
    kwargs.update({
        'pk': pk,
        'published': True
    })
    try:
        return get_object_or_404(Topology, **kwargs)
    except ValueError:
        raise Http404()
