import os
import sys
import logging
from django.test.runner import DiscoverRunner
from contextlib import contextmanager

try:
    from cStringIO import StringIO  # noqa
except ImportError:
    from io import StringIO  # noqa


@contextmanager
def redirect_stdout(stream):
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = sys.__stdout__


class LoggingDisabledTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        # disable logging below CRITICAL while testing
        logging.disable(logging.CRITICAL)
        return super(LoggingDisabledTestRunner, self).run_tests(test_labels,
                                                                extra_tests,
                                                                **kwargs)


class UnpublishMixin(object):
    def _unpublish(self):
        from ..models import Topology
        t = Topology.objects.first()
        t.published = False
        t.save()


class LoadMixin(object):
    def _load(self, file):
        d = os.path.dirname(os.path.abspath(__file__))
        return open(os.path.join(d, file)).read()
