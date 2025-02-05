import datetime

from django.core.management.base import BaseCommand
from django.db import connection

from core.logger import log

from inpx.utils import updateDBStatistic


class Command(BaseCommand):
    help = 'Clear database'

    def handle(self, **kwargs):
        success_message = "Database was cleared successfuly"
        error_message = "Cannot clear database table '{table}' because of error: {error}"

        start = datetime.datetime.now()
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

        time_spent = datetime.datetime.now() - start
        statistic = {
            'books_parsed': 0,
            'parse_errors': 0,
            'time_spent_parse': datetime.timedelta(seconds=0),
            'inps_created': 0,
            'inps_updated': 0,
            'series_created': 0,
            'authors_created': 0,
            'books_created': 0,
            'books_updated': 0,
            'time_spent_update': time_spent,
            'time_spent': time_spent,
            'file': ''
        }

        updateDBStatistic(statistic)
