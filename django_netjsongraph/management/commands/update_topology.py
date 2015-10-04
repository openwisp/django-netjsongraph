from django.core.management.base import BaseCommand

from ...utils import update_topology


class Command(BaseCommand):
    help = 'Update network topology'

    def add_arguments(self, parser):
        parser.add_argument('--label',
                            action='store',
                            default=None,
                            help='Will update topologies containing label')

    def handle(self, *args, **options):
        update_topology(options['label'])
