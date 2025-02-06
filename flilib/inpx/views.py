import datetime

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.db import connection

from django_tables2 import SingleTableView

from .models import Statistic
from .tables import StatisticTable
from .utils import Inpx, updateDBStatistic

# Create your views here.


class StatisticList(SingleTableView):
    model = Statistic
    table_class = StatisticTable
    table_pagination = {'per_page': 300}
    template_name = 'inpx/statistic_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_last'] = Statistic.objects.last()
        return context


class DbUpdate(TemplateView):
    template_name = 'inpx/update.html'
    inpxFileName = settings.INPX_FILE
    debug = settings.DEBUG

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inpx = Inpx(
            debug_performance=self.debug,
            update_db=True,
            verify_data=True,
        )
        context.update(inpx.process(self.inpxFileName))
        return context


class DbClear(TemplateView):
    template_name = 'inpx/clear.html'

    def post(self, request, *args, **kwargs):
        success_message = _("Database was cleared successfuly")
        error_message = _("Cannot clear database '{table}' because of error: {error}")

        start = datetime.datetime.now()
        try:
            with connection.cursor() as cursor:
                for table in ('bookauthor', 'bookgenre', 'book', 'author', 'series'):
                    cursor.execute(f'DELETE FROM library_{table}')

                table = 'inp'
                cursor.execute(f'DELETE FROM inpx_{table}')

                table = ''
                cursor.execute('VACUUM')

            messages.success(request, success_message)
        except Exception as e:
            messages.error(request, error_message.format(error=e, table=table))

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
        return HttpResponseRedirect('/')
