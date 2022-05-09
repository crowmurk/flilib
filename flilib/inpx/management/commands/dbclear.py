import time

from django.core.management.base import BaseCommand
from django.db import connection

from core.logger import log

from inpx.utils import updateStatistic

class Command(BaseCommand):
    help = 'Clear database'

    def handle(self, **kwargs):
        success_message = "Database was cleared successfuly"
        error_message = "Cannot clear database table '{table}' because of error: {error}"

        start = time.time()
        try:
            with connection.cursor() as cursor:
                for table in ('bookauthor', 'bookgenre', 'book', 'author', 'series'):
                    cursor.execute(f'DELETE FROM library_{table}')

                table = 'inp'
                cursor.execute(f'DELETE FROM inpx_{table}')

                table = ''
                cursor.execute('VACUUM')

            log.info(success_message)
        except Exception as e:
            log.error(error_message.format(error=e, table=table))

        updateStatistic(round(time.time() - start, 2))
