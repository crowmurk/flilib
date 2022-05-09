import time

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.db import connection

from .models import Statistic
from .utils import Inpx, updateStatistic

# Create your views here.

class DbStatistic(TemplateView):
    template_name = 'inpx/statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Statistic.objects.last()
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

        start = time.time()
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

        updateStatistic(round(time.time() - start, 2))
        return HttpResponseRedirect('/')
