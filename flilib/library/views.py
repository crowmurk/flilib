from django import forms
from django.views.generic import DetailView, View

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from core.views import FilteredTableMixin

from .utils import TableDownloadBookMixin, DownloadBookMixin

from .models import (
    Author,
    Genre,
    Language,
    Series,
    Book,
)

from .tables import (
    AuthorTable,
    GenreTable,
    LanguageTable,
    SeriesTable,
    BookTable,
)
from .filters import (
    AuthorFilter,
    GenreFilter,
    LanguageFilter,
    SeriesFilter,
    BookFilter,
)

# Create your views here.


class AuthorList(SingleTableMixin, FilterView):
    model = Author
    queryset = Author.objects.with_books_count()
    table_class = AuthorTable
    filterset_class = AuthorFilter
    table_pagination = {'per_page': 300}
    template_name = 'library/author_list.html'


class AuthorDetail(TableDownloadBookMixin, FilteredTableMixin, DetailView):
    model = Author
    table_class = BookTable
    filterset_class = BookFilter
    table_pagination = {'per_page': 300}
    related_name = 'authors'
    action = 'books_download'

    def get_table_kwargs(self):
        return {'exclude': ('authors', 'seriesnumber')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.fields['authors'].widget = forms.HiddenInput()
        return context


class GenreList(SingleTableMixin, FilterView):
    model = Genre
    queryset = Genre.objects.with_books_count()
    table_class = GenreTable
    filterset_class = GenreFilter
    table_pagination = False
    template_name = 'library/genre_list.html'


class GenreDetail(DetailView):
    model = Genre


class LanguageList(SingleTableMixin, FilterView):
    model = Language
    queryset = Language.objects.with_books_count()
    table_class = LanguageTable
    filterset_class = LanguageFilter
    table_pagination = False
    template_name = 'library/language_list.html'


class LanguageDetail(DetailView):
    model = Language


class SeriesList(SingleTableMixin, FilterView):
    model = Series
    queryset = Series.objects.with_books_count()
    table_class = SeriesTable
    filterset_class = SeriesFilter
    table_pagination = {'per_page': 300}
    template_name = 'library/series_list.html'


class SeriesDetail(TableDownloadBookMixin, FilteredTableMixin, DetailView):
    model = Series
    table_class = BookTable
    filterset_class = BookFilter
    table_pagination = {'per_page': 300}
    related_name = 'series'
    action = 'books_download'


class BookList(TableDownloadBookMixin, SingleTableMixin, FilterView):
    model = Book
    table_class = BookTable
    filterset_class = BookFilter
    table_pagination = {'per_page': 300}
    template_name = 'library/book_list.html'
    action = 'books_download'

    def get_table_kwargs(self):
        return {'exclude': ('seriesnumber', )}


class BookDetail(DetailView):
    model = Book

class BookDownload(DownloadBookMixin, View):
    model = Book
