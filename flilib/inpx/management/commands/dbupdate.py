from django.conf import settings
from django.core.management.base import BaseCommand

from ...utils import Inpx

class Command(BaseCommand):
    help = 'Upload inpx file to DB'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=settings.INPX_FILE,
            help='Path to inpx file',
        )

        parser.add_argument(
            '--debug-performance',
            action='store_true',
            help='Evaluate performance',
        )

        parser.add_argument(
            '--show-sql',
            action='store_true',
            help='Show SQL queries',
        )

        parser.add_argument(
            '--verify-data',
            action='store_true',
            help='Verify data before database update',
        )

        parser.add_argument(
            '--update-db',
            action='store_true',
            help='Update database',
        )

    def handle(self, **kwargs):
        file = kwargs.get('file', settings.INPX_FILE)

        kwargs = {
            key: value for key, value in kwargs.items()
            if key in (
                'verbosity',
                'debug_performance',
                'show_sql',
                'verify_data',
                'update_db',
            )
        }

        inpx = Inpx(**kwargs)
        inpx.process(file)
