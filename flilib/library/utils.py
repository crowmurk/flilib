import zipfile
import os
import io

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.encoding import escape_uri_path


class TableDownloadBookMixin:
    action_button = "action-table-button"
    action = None

    def post(self, request, *args, **kwargs):
        button = request.POST.get(self.action_button)
        pks = request.POST.getlist(button)

        if pks:
            selected_objects = self.table_class._meta.model.objects.filter(pk__in=pks,)

            if self.action:
                if hasattr(self, self.action):
                    return getattr(self, self.action)(request.path, selected_objects)

        return HttpResponseRedirect(request.path)

    def books_download(self, path, books):
        library = settings.LIBRARY_DIR
        files = {}

        for book in books:
            archiveFileName = os.path.join(library, book.archive.file) + '.zip'
            bookFileName = '.'.join((book.file, book.extension))

            if zipfile.Path(archiveFileName, bookFileName).is_file():
                if not files.get(archiveFileName):
                    files[archiveFileName] = []

                outFileName = book.get_download_name()
                outArchivePath = os.path.join(
                    str(book.authors.first()),
                    book.series.name if getattr(book, 'series') else '',
                )

                files[archiveFileName].append((
                    bookFileName,
                    outArchivePath,
                    outFileName,
                ))

        response = HttpResponse(content_type='application/zip')
        with zipfile.ZipFile(response, 'w') as responseFile:
            for archiveFileName, books in files.items():
                with zipfile.ZipFile(archiveFileName) as archiveFile:
                    for bookFileName, outArchivePath, outFileName in books:
                        with archiveFile.open(bookFileName) as bookFile:
                            book = bookFile.read()
                            buffer = io.BytesIO()
                            with zipfile.ZipFile(buffer, 'w') as bufferFile:
                                bufferFile.writestr(outFileName, book)
                            responseFile.writestr(
                                os.path.join(outArchivePath, outFileName + '.zip'),
                                buffer.getvalue(),
                            )

        response['Content-Disposition'] = 'attachment; filename=books.zip'
        return response


class DownloadBookMixin:
    pk_url_kwarg = 'pk'

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)

        if pk is None:
            raise AttributeError(
                "Generic view %s must be called with a pk."
                % self.__class__.__name__
            )
        return get_object_or_404(
            self.model,
            pk=pk,
        )

    def get(self, *args, **kwargs):
        library = settings.LIBRARY_DIR
        book = self.get_object()

        archiveFileName = os.path.join(library, book.archive.file) + '.zip'
        bookFileName = '.'.join((book.file, book.extension))

        if zipfile.Path(archiveFileName, bookFileName).is_file():
            outFileName = book.get_download_name()
            outArchiveFileName = escape_uri_path(outFileName + '.zip')

            response = HttpResponse(content_type='application/zip')
            with zipfile.ZipFile(response, 'w') as responseFile:
                with zipfile.ZipFile(archiveFileName) as archiveFile:
                    with archiveFile.open(bookFileName) as bookFile:
                        book = bookFile.read()
                    responseFile.writestr(outFileName, book)

            response['Content-Disposition'] = f"attachment; filename*=utf-8''{outArchiveFileName}"
            return response
        raise Http404(f'{self.model._meta.verbose_name} does not exists in library.')
