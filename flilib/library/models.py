from django.db import models
from django.db.models import Count, Q, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce

from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.core.validators import (
    validate_unicode_slug,
    MinValueValidator,
    MaxValueValidator,
)

from core.validators import validate_slug
from core.utils import get_unique_slug

# Create your models here.

class AuthorManager(models.Manager):
    use_in_migrations = True

    def with_books_count(self):
        return self.annotate(
            books_count=Count('books'),
        )

    def with_library_books_count(self):
        subquery = Subquery(
            Book.objects.filter(authors=OuterRef('id'), deleted=False)
            .order_by()
            .values('authors')
            .annotate(count=Count('pk'))
            .values('count'), output_field=IntegerField()
        )
        return self.annotate(books_count=Coalesce(subquery, 0))


class Author(models.Model):
    firstname = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_('Firstname'),
    )
    middlename = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_('Middlename'),
    )
    lastname = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_('Lastname'),
    )
    slug = models.SlugField(
        max_length=512,
        unique=True,
        editable=False,
        allow_unicode=True,
        validators=(
            validate_slug,
            validate_unicode_slug,
        ),
        help_text=_('A label for URL config.'),
    )

    objects = AuthorManager()

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ('lastname', 'firstname', 'middlename')
        unique_together = (('lastname', 'firstname', 'middlename'), )
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_all_names_are_blank",
                check=Q(lastname__gt='') | Q(firstname__gt='') | Q(middlename__gt=''),
            ),
        ]

    def __str__(self):
        return ' '.join(
            (self.lastname, self.firstname, self.middlename)
        ).strip()

    def clean(self):
        if not any((self.lastname, self.firstname, self.middlename)):
            message = _('At least one of the names required')
            raise ValidationError({
                'lastname': message,
                'firstname': message,
                'middlename': message,
            })

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(
            self,
            'slug',
            *('lastname', 'firstname', 'middlename'),
            unique=True,
        )
        super(Author, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'library:author:detail',
            kwargs={'slug': self.slug},
        )


class GenreManager(models.Manager):
    use_in_migrations = True

    def with_books_count(self):
        return self.annotate(
            books_count=Count('books'),
        )

    def with_library_books_count(self):
        subquery = Subquery(
            Book.objects.filter(genres=OuterRef('id'), deleted=False)
            .order_by()
            .values('genres')
            .annotate(count=Count('pk'))
            .values('count'), output_field=IntegerField()
        )
        return self.annotate(books_count=Coalesce(subquery, 0))


class Genre(models.Model):
    code = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_('Code'),
    )
    description = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_('Description'),
    )

    slug = models.SlugField(
        max_length=64,
        unique=True,
        editable=False,
        validators=(
            validate_slug,
        ),
        help_text=_('A label for URL config.'),
    )

    objects = GenreManager()

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        ordering = ('description', )

    def __str__(self):
        return ' - '.join(
            (self.code, self.description, )
        )

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(
            self,
            'slug',
            *('code', ),
            unique=True,
        )
        super(Genre, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'library:genre:detail',
            kwargs={'slug': self.slug},
        )


class LanguageManager(models.Manager):
    use_in_migrations = True

    def with_books_count(self):
        return self.annotate(
            books_count=Count('books'),
        )

    def with_library_books_count(self):
        subquery = Subquery(
            Book.objects
            .filter(language_id=OuterRef('id'), deleted=False)
            .order_by()
            .values('language')
            .annotate(count=Count('pk'))
            .values('count'), output_field=IntegerField()
        )
        return self.annotate(books_count=Coalesce(subquery, 0))


class Language(models.Model):
    code = models.CharField(
        max_length=2,
        unique=True,
        verbose_name=_('Code'),
    )
    name = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_('Name'),
    )

    slug = models.SlugField(
        max_length=2,
        unique=True,
        editable=False,
        validators=(
            validate_slug,
        ),
        help_text=_('A label for URL config.'),
    )

    objects = LanguageManager()

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ('name', )

    def __str__(self):
        return ' - '.join(
            (self.code, self.name, )
        )

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(
            self,
            'slug',
            *('code', ),
            unique=True,
        )
        super(Language, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'library:language:detail',
            kwargs={'slug': self.slug},
        )


class SeriesManager(models.Manager):
    use_in_migrations = True

    def with_books_count(self):
        return self.annotate(
            books_count=Count('books'),
        )

    def with_library_books_count(self):
        subquery = Subquery(
            Book.objects
            .filter(series_id=OuterRef('id'), deleted=False)
            .order_by()
            .values('series')
            .annotate(count=Count('pk'))
            .values('count'), output_field=IntegerField()
        )
        return self.annotate(books_count=Coalesce(subquery, 0))


class Series(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name=_('Name'),
    )
    slug = models.SlugField(
        max_length=256,
        unique=True,
        editable=False,
        allow_unicode=True,
        validators=(
            validate_slug,
            validate_unicode_slug,
        ),
        help_text=_('A label for URL config.'),
    )

    objects = SeriesManager()

    class Meta:
        verbose_name = pgettext_lazy('series model verbose', 'Series')
        verbose_name_plural = pgettext_lazy('series model verbose plural', 'Series')
        ordering = ('name', )
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s.name_required",
                check=Q(name__gt=''),
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(
            self,
            'slug',
            *('name', ),
            unique=True,
        )
        super(Series, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'library:series:detail',
            kwargs={'slug': self.slug},
        )


class BookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'authors', 'genres',
        ).select_related(
            'series', 'language', 'archive'
        )


class Book(models.Model):
    title = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_('Title'),
    )
    authors = models.ManyToManyField(
        Author,
        blank=True,
        related_name='books',
        through='BookAuthor',
        through_fields=('book', 'author'),
        verbose_name=_('Authors'),
    )
    genres = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='books',
        through='BookGenre',
        through_fields=('book', 'genre'),
        verbose_name=_('Genres'),
    )
    series = models.ForeignKey(
        Series,
        null=True,
        blank=True,
        related_name='books',
        on_delete=models.PROTECT,
        verbose_name=pgettext_lazy('book series verbose', 'Series'),
    )
    seriesnumber = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Series number'),
    )
    file = models.CharField(
        max_length=256,
        verbose_name=_('File'),
    )
    size = models.PositiveIntegerField(
        verbose_name=_('Size'),
    )
    libraryid = models.PositiveIntegerField(
        unique=True,
        verbose_name=_('Library ID'),
    )
    deleted = models.BooleanField(
        verbose_name=_('Deleted'),
    )
    extension = models.CharField(
        blank=True,
        max_length=8,
        verbose_name=_('Extension'),
    )
    date = models.DateField(
        verbose_name=_('Date'),
    )
    language = models.ForeignKey(
        Language,
        null=True,
        blank=True,
        related_name='books',
        on_delete=models.PROTECT,
        verbose_name=_('Language'),
    )
    libraryrate = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(5),
        ),
        verbose_name=_('Library rate'),
    )
    keywords = models.CharField(
        max_length=512,
        blank=True,
        verbose_name=_('Keywords'),
    )
    archive = models.ForeignKey(
        'inpx.Inp',
        related_name='books',
        on_delete=models.PROTECT,
        verbose_name=_('Archive'),
    )

    objects = BookManager()

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s.seriesnumber_without_series",
                check=Q(series__isnull=True, seriesnumber__isnull=True) | Q(series__isnull=False),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s.file_required",
                check=Q(file__gt=''),
            )
        ]

    def __str__(self):
        return _("{book} by {authors}").format(
            book=self.title,
            authors=', '.join(str(item) for item in self.authors.all()),
        )

    def clean(self):
        if not self.series and isinstance(self.seriesnumber, int):
            raise ValidationError({
                'series': _('Series required.'),
                'seriesnumber': _('Series number without series'),
            })

    def get_absolute_url(self):
        return reverse(
            'library:book:detail',
            kwargs={'pk': self.pk},
        )

    def get_download_name(self):
        return f'{self.authors.first()} - {self.title} ({self.libraryid}).{self.extension}'

    def get_download_url(self):
        return reverse(
            'library:book:download',
            kwargs={'pk': self.pk},
        )


class BookAuthor(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = (('book', 'author'), )


class BookGenre(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = (('book', 'genre'), )
