from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from .models import Statistic


class StatisticTable(tables.Table):
    time_spent = tables.Column(
        attrs={
            "th": {"class": "text-end"},
            "td": {"class": "text-end"},
        },
    )

    class Meta:
        model = Statistic
        fields = (
            'date',
            'authors_created',
            'series_created',
            'books_created',
            'books_updated',
            'time_spent',
        )
        template_name = "core/table.html"
        empty_text = _("There are no records available")
