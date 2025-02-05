import datetime
import hashlib
import multiprocessing
import os
import re
import zipfile

from django.db import transaction
from django.utils.functional import cached_property

from core.debugers import query_debugger, performance_debugger
from core.logger import log
from core.utils import Slug

from library.models import (
    Author,
    Genre,
    Language,
    Series,
    Book,
    BookAuthor,
    BookGenre,
)

from .models import GenreAlias, LanguageAlias, Inp, Statistic


def renumerate(collection):
    for i in range(len(collection) - 1, -1, -1):
        yield i, collection[i]


def updateDBStatistic(statistic):
    start = datetime.datetime.now()

    statistic.update({
        'authors_database': Author.objects.all().count(),
        'authors_library': Author.objects.with_library_books_count().filter(books_count__gt=0).count(),

        'genres_database': Genre.objects.with_books_count().filter(books_count__gt=0).count(),
        'genres_library': Genre.objects.with_library_books_count().filter(books_count__gt=0).count(),

        'languages_database': Language.objects.with_books_count().filter(books_count__gt=0).count(),
        'languages_library': Language.objects.with_library_books_count().filter(books_count__gt=0).count(),

        'series_database': Series.objects.all().count(),
        'series_library': Series.objects.with_library_books_count().filter(books_count__gt=0).count(),

        'books_database': Book.objects.all().count(),
        'books_library': Book.objects.filter(deleted=False).count(),
    })

    time_spent_statistic = datetime.datetime.now() - start
    statistic['time_spent_update'] += time_spent_statistic
    statistic['time_spent'] += time_spent_statistic

    Statistic.objects.create(**statistic)

    return statistic


class Inpx:
    fieldSeparator = b'\x04'
    itemSeparator = ':'
    nameSeparator = ','
    fields = (
        'authors',
        'genres',
        'title',
        'series',
        'seriesnumber',
        'file',
        'size',
        'libraryid',
        'deleted',
        'extension',
        'date',
        'language',
        'libraryrate',
        'keywords',
    )
    authorFields = (
        'lastname',
        'firstname',
        'middlename',
    )
    libraryrates = {1, 2, 3, 4, 5}

    def __new__(cls, **kwargs):
        if kwargs.get('debug_performance', False):
            for method in ('load', 'parse', 'prepare', 'verify'):
                setattr(cls, method, performance_debugger(
                    getattr(cls, method)
                ))
            setattr(cls, 'updateDBStatistic', staticmethod(query_debugger(
                show_sql=kwargs.get('show_sql')
            )(updateDBStatistic)))
        else:
            setattr(cls, 'updateDBStatistic', staticmethod(updateDBStatistic))

        return super().__new__(cls)

    def __init__(self, **kwargs):
        self.debug_performance = kwargs.get('debug_performance', False)
        self.show_sql = kwargs.get('show_sql', False)
        self.verify_data = kwargs.get('verify_data', False)
        self.update_db = kwargs.get('update_db', False)
        self.verbosity = kwargs.get('verbosity', 1)

        self.inp_files = {}
        self.books = []
        self.errors = []

    @cached_property
    def languages_codes(self):
        return tuple(
            Language.objects.values_list('code', flat=True)
        )

    @cached_property
    def genres_codes(self):
        return tuple(
            Genre.objects.values_list('code', flat=True)
        )

    @cached_property
    def language_aliases(self):
        return {
            code: language for code, language in
            LanguageAlias.objects.values_list('code', 'language__code')
        }

    @cached_property
    def genre_aliases(self):
        return {
            code: genre for code, genre in
            GenreAlias.objects.values_list('code', 'genre__code')
        }

    def load(self, inpxFileName):
        data = []

        inp_files = {
            file: mdhash
            for file, mdhash in Inp.objects.values_list('file', 'mdhash')
        }

        with zipfile.ZipFile(inpxFileName, 'r') as inpx:
            for inpFileName in inpx.namelist():
                fileName, fileExt = os.path.splitext(inpFileName)
                if fileExt.lower() == '.inp':
                    with inpx.open(inpFileName, 'r') as inp:
                        file = inp.read()
                        mdhash = hashlib.md5(file).hexdigest()
                        if mdhash != inp_files.get(fileName):
                            inp_files[fileName] = mdhash
                            data.append((fileName, file))

        self.inp_files = inp_files
        return data

    def parse(self, data):
        workers = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=workers)

        for items in pool.map(self._parser, data):
            self.books.extend(items)

    def _parser(self, rawData):
        books = []

        fileName, data = rawData

        for line in data.splitlines():
            line = map(bytes.decode, line.split(self.fieldSeparator))
            line = map(str.strip, line)
            line = dict(zip(self.fields, line))

            # Authors
            line['authors'] = [
                author.strip(self.nameSeparator).split(self.nameSeparator)
                for author in line['authors'].strip(self.itemSeparator).split(self.itemSeparator)
            ]
            line['authors'] = [
                dict(zip(self.authorFields, author + [''] * (len(self.authorFields) - len(author))))
                for author in line['authors'] if any(author)
            ]

            # Genres
            line['genres'] = line['genres'].strip(self.itemSeparator).split(self.itemSeparator)
            line['genres'] = [genre for genre in line['genres'] if genre]

            # Seriesnumber, Size, Libraryid, Libraryrate
            for field in ('seriesnumber', 'size', 'libraryid', 'libraryrate', ):
                try:
                    line[field] = int(line[field])
                except ValueError:
                    pass

            # Deleted
            try:
                line['deleted'] = int(line['deleted'])
            except ValueError:
                pass
            else:
                line['deleted'] = bool(line['deleted'])

            # Date
            try:
                line['date'] = datetime.datetime.fromisoformat(line['date'])
            except ValueError:
                pass

            # Archive
            line['archive'] = fileName

            books.append(line)

        return books

    def prepare(self):
        bookids = set()

        name_in_seriesnumber = re.compile(r'^« name=»(.+)$')
        space_in_seriesnumber = re.compile(r'^(?:\d+\s*)+$')

        for book_index, book in renumerate(self.books):
            # Genres
            for index, genre in enumerate(book['genres']):
                if genre not in self.genres_codes:
                    book['genres'][index] = self.genre_aliases.get(genre, '')

            book['genres'] = list(set([genre for genre in book['genres'] if genre]))

            # Seriesnumber
            if not isinstance(book['seriesnumber'], int):
                if book['seriesnumber']:
                    search = name_in_seriesnumber.findall(book['seriesnumber'])
                    if search:
                        book['series'] = search[0]
                        book['seriesnumber'] = ''
                    elif space_in_seriesnumber.match(book['seriesnumber']):
                        book['seriesnumber'] = int(''.join(book['seriesnumber'].split()))
                    else:
                        book['seriesnumber'] = ''

            if book['seriesnumber'] != '' and book['series'] == '':
                book['seriesnumber'] = ''

            # Libraryid
            libraryid = book.get('libraryid')
            if libraryid in bookids:
                self.books.pop(book_index)
                continue
            else:
                bookids.add(libraryid)

            # Deleted
            if book['deleted'] == '':
                book['deleted'] = False

            # Language
            if book['language'] not in self.languages_codes:
                book['language'] = self.language_aliases.get(book['language'], '')

            # Libraryrate
            if not isinstance(book['libraryrate'], int):
                book['libraryrate'] = ''

            self.books[book_index] = {
                key: value for key, value in book.items()
                if isinstance(value, (bool, int)) or value
            }

    def _add_error(self, index, reason):
        self.errors.append({'reason': reason, 'data': self.books.pop(index), })
        if self.verbosity == 2:
            log.error('Parse book: {error}'.format(error=self.errors[-1]))

    def verify(self):
        bookids = set()

        for index, book in renumerate(self.books):
            error = False

            # Authors
            authors = book.get('authors', [])
            authors_values = [author.values() for author in authors]

            if len(authors_values) != len(set(authors_values)):
                self._add_error(index, 'authors')
                continue

            for author in authors:
                if not any(author.values()):
                    error = True
                    break
            if error:
                self._add_error(index, 'authors')
                continue

            # Genres
            genres = book.get('genres', [])

            if len(genres) != len(set(genres)):
                self._add_error(index, 'genres')
                continue

            for genre in genres:
                if genre not in self.genres_codes:
                    error = True
                    break
            if error:
                self._add_error(index, 'genres')
                continue

            # Seriesnumber
            seriesnumber = book.get('seriesnumber')
            if not (isinstance(seriesnumber, int) or seriesnumber is None):
                self._add_error(index, 'seriesnumber')
                continue

            if seriesnumber is not None and not book.get('series'):
                self._add_error(index, 'seriesnumber')
                continue

            # File
            if not book.get('file'):
                self._add_error(index, 'file')
                continue

            # Size
            if not isinstance(book.get('size'), int):
                self._add_error(index, 'size')
                continue

            # Libraryid
            libraryid = book.get('libraryid')
            if not isinstance(libraryid, int):
                self._add_error(index, 'libraryid')
                continue

            if libraryid in bookids:
                self._add_error(index, 'libraryid')
                continue
            else:
                bookids.add(libraryid)

            # Deleted
            if not isinstance(book.get('deleted'), bool):
                self._add_error(index, 'deleted')
                continue

            # Date
            if not isinstance(book.get('date'), datetime.date):
                self._add_error(index, 'date')
                continue

            # Language
            language = book.get('language')
            if language and language not in self.languages_codes:
                self._add_error(index, 'language')

            # Libraryrate
            libraryrate = book.get('libraryrate')
            if isinstance(libraryrate, int) and libraryrate not in self.libraryrates:
                self._add_error(index, 'libraryrate')

    def db_update(self):
        return UpdateDB(self).process()

    def process(self, inpxFileName):
        results = {}
        start = datetime.datetime.now()

        if self.verbosity == 1:
            log.info('Start parsing inpx...')
            log.info('File: {file}'.format(file=inpxFileName))

        self.parse(self.load(inpxFileName))

        if self.update_db:
            self.prepare()
            if self.verify_data:
                self.verify()

        parser_results = {
            'books_parsed': len(self.books),
            'parse_errors': len(self.errors),
            'time_spent_parse': datetime.datetime.now() - start,
        }
        results.update(parser_results)
        results['file'] = inpxFileName

        if self.verbosity == 1:
            log.info('Books parsed: {books_parsed}. Errors: {parse_errors}. Time spent {time_spent_parse}.'.format(
                **parser_results
            ))

        if self.update_db:
            update_results = self.db_update()

            results.update(update_results)
            results['time_spent'] = results['time_spent_parse'] + results['time_spent_update']

            results = self.updateDBStatistic(results)
        else:
            results['time_spent_update'] = datetime.timedelta(seconds=0)

        results['time_spent'] = datetime.datetime.now() - start

        return results


class UpdateDB:
    def __new__(cls, inpx):
        if inpx.debug_performance:
            for method in ('inps', 'series', 'authors', 'books'):
                setattr(cls, method, query_debugger(
                    show_sql=inpx.show_sql
                )(getattr(cls, method)))
        return super().__new__(cls)

    def __init__(self, inpx):
        self.inpx = inpx

    def inps(self):
        inp_exist = Inp.objects.values_list('file', flat=True)

        inp_create = [Inp(**{'file': file, 'mdhash': mdhash})
                      for file, mdhash in self.inpx.inp_files.items()
                      if file not in inp_exist]

        inp_update = Inp.objects.filter(
            file__in=self.inpx.inp_files.keys(),
        ).exclude(
            mdhash__in=self.inpx.inp_files.values(),
        ).values_list('file', flat=True)

        update_data = [(file, mdhash) for file, mdhash in self.inpx.inp_files.items()
                       if file in inp_update]

        inp_update = [Inp.objects.get(file=file) for file, mdhash in update_data]

        for index, data in enumerate(update_data):
            inp_update[index].mdhash = data[-1]

        try:
            inps_updated = Inp.objects.bulk_update(inp_update, ['mdhash'])
        except Exception as error:
            log.error("Inp update error ({type}): {error}".format(
                error=error,
                type=type(error).__name__,
            ))
            return 0, 0

        try:
            inps_created = len(Inp.objects.bulk_create(inp_create))
        except Exception as error:
            log.error("Inp create error ({type}): {error}".format(
                error=error,
                type=type(error).__name__,
            ))
            return 0, 0

        return inps_created, inps_updated

    def series(self):
        series_exists = set(Series.objects.values_list('name', flat=True))
        series_data = set(book.get('series', '') for book in self.inpx.books)

        series_create = [
            Series(name=series) for series in series_data.difference(series_exists) if series
        ]

        Slug('slug', 'name', unique=True).bulk_slugify(series_create)

        try:
            return len(Series.objects.bulk_create(series_create))
        except Exception as error:
            log.error("Series create error ({type}): {error}".format(
                error=error,
                type=type(error).__name__,
            ))
            return 0

    def authors(self):
        authors_exists = set(Author.objects.values_list(*self.inpx.authorFields))
        authors_data = set(
            tuple(author.values())
            for book in self.inpx.books
            for author in book.get('authors', [])
        )

        authors_create = [
            Author(**dict(zip(self.inpx.authorFields, author)))
            for author in authors_data.difference(authors_exists)
        ]

        Slug(
            'slug',
            *self.inpx.authorFields,
            unique=True,
        ).bulk_slugify(authors_create)

        try:
            return len(Author.objects.bulk_create(authors_create))
        except Exception as error:
            log.error("Authors create error ({type}): {error}".format(
                error=error,
                type=type(error).__name__,
            ))
            return 0

    def books(self):
        authors = {
            (lastname, firstname, middlename): id_
            for id_, lastname, firstname, middlename in
            Author.objects.values_list('id', *self.inpx.authorFields)
        }
        genres = dict(Genre.objects.values_list('code', 'id'))
        series = dict(Series.objects.values_list('name', 'id'))
        languages = dict(Language.objects.values_list('code', 'id'))
        archives = dict(Inp.objects.values_list('file', 'id'))

        # Create books
        books_exists = set(Book.objects.values_list('libraryid', flat=True))
        create_data = [book for book in self.inpx.books if book['libraryid'] not in books_exists]

        for book in create_data:
            book['authors_ids'] = [authors[tuple(author.values())] for author in book.pop('authors', [])]
            book['genres_ids'] = [genres[genre] for genre in book.pop('genres', [])]

            if book.get('series'):
                book['series_id'] = series[book.pop('series')]
            if book.get('language'):
                book['language_id'] = languages[book.pop('language')]
            if book.get('archive'):
                book['archive_id'] = archives[book.pop('archive')]

        books_create = [Book(**{key: value for key, value in book.items() if key not in (
            'authors_ids',
            'genres_ids',
        )}) for book in create_data]

        try:
            books_created = Book.objects.bulk_create(books_create)
        except Exception as error:
            log.error("Books create error ({type}): {error}".format(
                error=error,
                type=type(error).__name__,
            ))
            return 0, 0

        # Create m2m
        books_created = {
            instance.libraryid: instance.id
            for instance in books_created
        }

        bookauthor_create = [
            BookAuthor(book_id=books_created[book['libraryid']], author_id=author)
            for book in create_data
            for author in book['authors_ids']
        ]

        try:
            BookAuthor.objects.bulk_create(bookauthor_create)
        except Exception as error:
            log.error("Authors m2m create error ({type}): {error}".format(
                error=error,
                type=type(error).__name__,
            ))
            return 0, 0

        bookgenre_create = [
            BookGenre(book_id=books_created[book['libraryid']], genre_id=genre)
            for book in create_data
            for genre in book['genres_ids']
        ]

        try:
            BookGenre.objects.bulk_create(bookgenre_create)
        except Exception as error:
            log.error("Genres m2m create error ({type}): {error}".format(
                error=error,
                type=type(error).__name__,
            ))
            return 0, 0

        # Update books status
        books_exists = set(Book.objects.values_list('libraryid', 'deleted'))
        update_data = [
            (book['libraryid'], book['deleted'])
            for book in self.inpx.books
            if (book['libraryid'], book['deleted']) not in books_exists
        ]

        books_update = [Book.objects.get(libraryid=libraryid) for libraryid, deleted in update_data]

        for index, data in enumerate(update_data):
            books_update[index].deleted = data[-1]

        try:
            books_updated = Book.objects.bulk_update(books_update, ['deleted'])
        except Exception as error:
            log.error("Book update error ({type}): {error}".format(
                error=error,
                type=type(error).__name__,
            ))
            return 0, 0

        return len(books_created), books_updated

    @transaction.atomic
    def process(self):
        results = {}
        start = datetime.datetime.now()

        if self.inpx.verbosity == 1:
            log.info('Start updating database...')

        results['inps_created'], results['inps_updated'] = self.inps()
        results['series_created'] = self.series()
        results['authors_created'] = self.authors()
        results['books_created'], results['books_updated'] = self.books()
        results['time_spent_update'] = datetime.datetime.now() - start

        if self.inpx.verbosity == 1:
            log.info(
                'Inps: created {inps_created}, updated {inps_updated}.'
                ' Series created: {series_created}.'
                ' Authors created: {authors_created}.'
                ' Books: created {books_created}, updated {books_updated}.'
                ' Time spent: {time_spent_update}.'.format(**results)
            )

        return results
