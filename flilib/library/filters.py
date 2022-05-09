from django import forms

from django.db.models import Q
from django.http.request import QueryDict
from django.utils.translation import gettext_lazy as _

import django_filters as filters

from .models import (
    Author,
    Genre,
    Language,
    Series,
    Book,
)


class AuthorFilter(filters.FilterSet):
    authors = filters.CharFilter(
        method='author_filter',
        label=_('Author'),
    )
    books = filters.LookupChoiceFilter(
        field_class=forms.DecimalField,
        widget=forms.NumberInput(attrs={'step': '1', 'min': 0}),
        field_name='books_count',
        lookup_choices=[
            ('exact', ('==')),
            ('gte', '>='),
            ('lte', '<='),
        ],
        empty_label=None,
        label=_('Books'),
    )

    class Meta:
        model = Author
        fields = []

    def author_filter(self, queryset, name, value):
        for word in value.split():
            queryset = queryset.filter(
                Q(firstname__iexact=word) | Q(middlename__iexact=word) | Q(lastname__iexact=word)
            )
        return queryset


class GenreFilter(filters.FilterSet):
    code = filters.CharFilter(
        label=_('Code'),
        lookup_expr='icontains',
    )
    description = filters.CharFilter(
        label=_('Description'),
        lookup_expr='icontains',
    )
    books = filters.LookupChoiceFilter(
        field_class=forms.DecimalField,
        widget=forms.NumberInput(attrs={'step': '1', 'min': 0}),
        field_name='books_count',
        lookup_choices=[
            ('exact', ('==')),
            ('gte', '>='),
            ('lte', '<='),
        ],
        empty_label=None,
        label=_('Books'),
    )

    class Meta:
        model = Genre
        fields = []


class LanguageFilter(filters.FilterSet):
    code = filters.CharFilter(
        label=_('Code'),
        lookup_expr='icontains',
    )
    name = filters.CharFilter(
        label=_('Language'),
        lookup_expr='icontains',
    )
    books = filters.LookupChoiceFilter(
        field_class=forms.DecimalField,
        widget=forms.NumberInput(attrs={'step': '1', 'min': 0}),
        field_name='books_count',
        lookup_choices=[
            ('exact', ('==')),
            ('gte', '>='),
            ('lte', '<='),
        ],
        empty_label=None,
        label=_('Books'),
    )

    class Meta:
        model = Language
        fields = []


class SeriesFilter(filters.FilterSet):
    name = filters.CharFilter(
        label=_('Name'),
        lookup_expr='icontains',
    )
    books = filters.LookupChoiceFilter(
        field_class=forms.DecimalField,
        widget=forms.NumberInput(attrs={'step': '1', 'min': 0}),
        field_name='books_count',
        lookup_choices=[
            ('exact', ('==')),
            ('gte', '>='),
            ('lte', '<='),
        ],
        empty_label=None,
        label=_('Books'),
    )

    class Meta:
        model = Series
        fields = []


class BookFilter(filters.FilterSet):
    authors = filters.CharFilter(
        method='author_filter',
        label=_('Author'),
    )
    title = filters.CharFilter(
        label=_('Title'),
        lookup_expr='icontains',
    )
    genres = filters.ChoiceFilter(
        choices=Genre.objects.values_list('id', 'description'),
        label=_('Genre'),
        empty_label=_('All genres'),
    )
    language = filters.ChoiceFilter(
        choices=Language.objects.values_list('id', 'name'),
        empty_label=_('All languages'),
    )
    libraryrate = filters.LookupChoiceFilter(
        method='libraryrate_filter',
        field_class=forms.DecimalField,
        widget=forms.NumberInput(attrs={'step': '1', 'min': 0}),
        lookup_choices=[
            ('exact', ('==')),
            ('gte', '>='),
            ('lte', '<='),
        ],
        empty_label=None,
    )
    deleted = filters.BooleanFilter(
        widget=forms.Select(
            choices=(
                ('', _('All')),
                (False, _('No')),
                (True, _('Yes')),
            ),
        ),
    )

    class Meta:
        model = Book
        fields = []

    def __init__(self, data=None, *args, **kwargs):
        if not data:
            data = QueryDict("deleted=False")

        super(BookFilter, self).__init__(data, *args, **kwargs)

    def author_filter(self, queryset, name, value):
        for word in value.split():
            queryset = queryset.filter(
                Q(authors__firstname__iexact=word) | Q(authors__middlename__iexact=word) | Q(authors__lastname__iexact=word)
            )
        return queryset

    def libraryrate_filter(self, queryset, name, lookup):
        kwargs = {f'{name}__{lookup.lookup_expr}': lookup.value}

        if lookup.lookup_expr == 'lte':
            return queryset.filter(Q(**kwargs) | Q(**{f'{name}__isnull': True}))

        return queryset.filter(**kwargs)
