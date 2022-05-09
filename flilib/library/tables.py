from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe

import django_tables2 as tables

from .models import (
    Author,
    Genre,
    Language,
    Series,
    Book,
)


class AuthorTable(tables.Table):
    lastname = tables.Column(linkify=True)
    books = tables.Column(
        accessor='books_count',
        verbose_name=_('Books'),
    )

    class Meta:
        model = Author
        fields = (
            'lastname',
            'firstname',
            'middlename',
            'books',
        )
        template_name = "core/table.html"
        empty_text = _("There are no records available")


class GenreTable(tables.Table):
    code = tables.Column(linkify=True)
    books = tables.Column(
        accessor='books_count',
        verbose_name=_('Books'),
    )

    class Meta:
        model = Genre
        fields = (
            'code',
            'description',
            'books',
        )
        template_name = "core/table.html"
        empty_text = _("There are no records available")


class LanguageTable(tables.Table):
    code = tables.Column(linkify=True)
    name = tables.Column(
        verbose_name=_('Language'),
    )
    books = tables.Column(
        accessor='books_count',
        verbose_name=_('Books'),
    )

    class Meta:
        model = Language
        fields = (
            'code',
            'name',
            'books',
        )
        template_name = "core/table.html"
        empty_text = _("There are no records available")


class SeriesTable(tables.Table):
    name = tables.Column(linkify=True)
    books = tables.Column(
        accessor='books_count',
        verbose_name=_('Books'),
    )

    class Meta:
        model = Series
        fields = (
            'name',
            'books',
        )
        template_name = "core/table.html"
        empty_text = _("There are no records available")


class BookTable(tables.Table):
    authors = tables.ManyToManyColumn(linkify_item=True)
    title = tables.Column(empty_values=())
    language = tables.Column(
        accessor='language.name',
        verbose_name=_('Language'),
    )
    genres = tables.ManyToManyColumn(
        transform=lambda g: g.description,
    )
    download = tables.CheckBoxColumn(
        accessor="pk",
    )

    class Meta:
        model = Book
        fields = (
            'authors',
            'title',
            'genres',
            'language',
            'libraryrate',
            'seriesnumber',
        )
        template_name = "core/table.html"
        empty_text = _("There are no records available")

    def render_title(self, record):
        return mark_safe('<a href="{url}">{text}</a>'.format(
            url=record.get_absolute_url(),
            text=record.title if record.title else '—',
        ))
