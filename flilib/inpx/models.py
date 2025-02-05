from django.db import models
from django.db.models import Q

from django.utils.translation import gettext_lazy as _

from library.models import Genre, Language

# Create your models here.

class Inp(models.Model):
    file = models.CharField(
        max_length=256,
        unique=True,
        verbose_name=_('File'),
    )
    mdhash = models.CharField(
        max_length=32,
        unique=True,
        verbose_name=_('Hash'),
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s.file_required",
                check=Q(file__gt=''),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s.mdhash_required",
                check=Q(mdhash__gt=''),
            ),
        ]


class GenreAlias(models.Model):
    code = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_('Code'),
    )
    genre = models.ForeignKey(
        Genre,
        related_name='aliases',
        on_delete=models.PROTECT,
        verbose_name=_('Gennre'),
    )


class LanguageAlias(models.Model):
    code = models.CharField(
        max_length=8,
        unique=True,
        verbose_name=_('Code'),
    )
    language = models.ForeignKey(
        Language,
        related_name='aliases',
        on_delete=models.PROTECT,
        verbose_name=_('Language'),
    )


class Statistic(models.Model):
    books_parsed = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Books parsed'),
    )
    parse_errors = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Parse errors'),
    )
    time_spent_parse = models.DurationField(
        editable=False,
        blank=True,
        verbose_name=_('Parse time spend'),
    )
    inps_created = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('INPS created'),
    )
    inps_updated = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('INPS updated'),
    )
    series_created = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Series creaated'),
    )
    authors_created = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Authors created'),
    )
    books_created = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Books created'),
    )
    books_updated = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Books updated'),
    )
    time_spent_update = models.DurationField(
        editable=False,
        blank=True,
        verbose_name=_('Update time spend'),
    )
    authors_database = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Authors in database'),
    )
    authors_library = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Authors in library'),
    )
    genres_database = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Genres in database'),
    )
    genres_library = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Genres in library'),
    )
    languages_database = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Languages in database'),
    )
    languages_library = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Languages in library'),
    )
    series_database = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Series in database'),
    )
    series_library = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Series in library'),
    )
    books_database = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Books in database'),
    )
    books_library = models.PositiveIntegerField(
        editable=False,
        blank=True,
        verbose_name=_('Books in library'),
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Update date'),
    )
    time_spent = models.DurationField(
        editable=False,
        blank=True,
        verbose_name=_('Update time spent'),
    )
    file = models.CharField(
        max_length=4096,
        editable=False,
        blank=True,
        verbose_name=_('INPX file'),
    )


    class Meta:
        verbose_name = _('Database statistic')
        verbose_name_plural = _('Database statistic')
        ordering = ('date', )
