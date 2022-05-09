import string
import inspect

from django.core.paginator import EmptyPage, InvalidPage
from django.db.models import Count
from django.db.models.functions import Substr
from django.utils.functional import cached_property
from django.utils.inspect import method_has_no_args
from django.utils.translation import gettext_lazy as _


class AlphabetPaginator:
    """Pagination for string-based objects.
    """
    non_alpha = '_'
    alphabet = string.ascii_uppercase

    def __init__(self, object_list, per_page, *args, **kwargs):
        self.object_list = object_list
        self.per_page = int(per_page)

        self.paginate_on = kwargs.pop('paginate_on', None)
        self.non_alpha = kwargs.get('non_alpha', self.non_alpha)

        self.alphabet = set(self.alphabet)
        self.alphabet.update(kwargs.get('alphabet', "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ").upper())
        self.alphabet = ''.join(sorted(self.alphabet))

        self.pages = self._get_pages()

    def _get_pages(self):
        pages = []

        fl_key = f'firstletter_{self.paginate_on}'
        fl_count = f'firstletter_{self.paginate_on}_count'

        counter = self.object_list.annotate(
            **{fl_key: Substr(self.paginate_on, 1, 1)}
        ).values(fl_key).annotate(
            **{fl_count: Count('id')}
        ).values_list(fl_key, fl_count)

        pages_dict = {}
        for key, value in counter:
            key_upper = key.upper()
            if key_upper in self.alphabet:
                pages_dict[key_upper] = pages_dict.get(key_upper, 0) + value
            else:
                pages_dict[self.non_alpha] = pages_dict.get(self.non_alpha, 0) + value

        page_letters = []

        page_count = pages_dict.get(self.non_alpha, 0)
        if page_count:
            page_letters.append(self.non_alpha)

        for letter in self.alphabet:
            letter_count = pages_dict.get(letter, 0)

            if letter_count + page_count > self.per_page:
                page_count = letter_count
                pages.append(page_letters)
                page_letters = [letter, ]
            else:
                page_count += letter_count
                page_letters.append(letter)

        pages.append(page_letters)

        return pages

    def __iter__(self):
        for page_number in self.page_range:
            yield self.page(page_number)

    def validate_letter(self, letter):
        try:
            letter = int(letter)
        except (TypeError, ValueError):
            pass
        else:
            if letter < 1:
                raise EmptyPage(_('That page letter is less than 1'))
            if letter > self.num_pages:
                raise EmptyPage(_('That page contains no results'))
            return self.pages[letter - 1]

        if letter == self.non_alpha or letter in self.alphabet:
            for page in self.pages:
                if letter in page:
                    return page
            raise EmptyPage(_('That page contains no results'))
        else:
            raise InvalidPage(_('Invalid page letter'))

    def get_page(self, page):
        try:
            page = self.validate_letter(page)
        except InvalidPage:
            page = self.pages[0]
        except EmptyPage:
            page = self.pages[-1]
        return self.page(page)

    def page(self, page):
        page = self.validate_letter(page)
        queryset = self.object_list.filter(
            **{'{}__iregex'.format(self.paginate_on): '^({}).*'.format('|'.join(page))}
        )
        return AlphabetPage(queryset, page, self)

    @cached_property
    def count(self):
        c = getattr(self.object_list, "count", None)
        if callable(c) and not inspect.isbuiltin(c) and method_has_no_args(c):
            return c()
        return len(self.object_list)

    @cached_property
    def num_pages(self):
        return len(self.pages)

    @property
    def page_range(self):
        return range(1, self.num_pages + 1)


class AlphabetPage:
    def __init__(self, object_list, page, paginator):
        self.object_list = object_list
        self.letters = page
        self.paginator = paginator

    def __repr__(self):
        if self.start_letter == self.end_letter:
            return self.start_letter
        else:
            if self.paginator.otherletters == self.end_letter:
                return '%c-%c' % (self.end_letter, self.start_letter)
            else:
                return '%c-%c' % (self.start_letter, self.end_letter)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        if not isinstance(index, (int, slice)):
            raise TypeError(
                'Page indices must be integers or slices, not %s.'
                % type(index).__name__
            )
        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    @property
    def start_letter(self):
        if len(self.letters) > 0:
            self.letters.sort(key=str.upper)
            return self.letters[0]
        else:
            return None

    @property
    def end_letter(self):
        if len(self.letters) > 0:
            self.letters.sort(key=str.upper)
            return self.letters[-1]
        else:
            return None

    @property
    def number(self):
        return self.paginator.pages.index(self.letters) + 1

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.paginator.validate_number(self.number + 1)

    def previous_page_number(self):
        return self.paginator.validate_number(self.number - 1)
