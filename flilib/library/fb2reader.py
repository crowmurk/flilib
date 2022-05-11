import zipfile
import os

import xml.etree.ElementTree as ET

from django.conf import settings

from .models import Book


class Fb2Reader:
    model = Book
    namespaces = {
        'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0',
        'l': 'http://www.w3.org/1999/xlink'
    }

    def __init__(self, book):
        self.book = self._get_book(book)

    def _get_book(self, book):
        library = settings.LIBRARY_DIR

        if isinstance(book, int):
            book = self.model.objects.get(pk=book)

        archiveFileName = os.path.join(library, book.archive.file) + '.zip'
        bookFileName = '.'.join((book.file, book.extension))

        if os.path.isfile(archiveFileName) and zipfile.Path(archiveFileName, bookFileName).is_file():
            with zipfile.ZipFile(archiveFileName) as archiveFile:
                with archiveFile.open(bookFileName) as bookFile:
                    file = bookFile.read()
                return ET.fromstring(file)
        return None

    def cover(self):
        try:
            name = self.book.find(
                'fb:description/fb:title-info/fb:coverpage/fb:image',
                namespaces=self.namespaces,
            )
            name_href = name.attrib[f'{{{self.namespaces["l"]}}}href'].lstrip('#')

            cover = self.book.find(
                f'fb:binary[@id="{name_href}"]',
                namespaces=self.namespaces,
            )
            return cover.text
        except (AttributeError, KeyError):
            return None
