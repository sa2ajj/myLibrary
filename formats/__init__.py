
from os import stat
from datetime import datetime

class BookInfo:
    def __init__(self, path):
        self._path = path
        self._stamp = None

    @staticmethod
    def supports(filename):
        raise NotImplemented

    @property
    def title(self):
        raise NotImplemented

    @property
    def authors(self):
        raise NotImplemented

    @property
    def series(self):
        raise NotImplemented

    @property
    def path(self):
        return self._path

    @property
    def stamp(self):
        if self._stamp is None:
            info = stat(self._path)

            self._stamp = datetime.fromtimestamp(info[8])

        return self._stamp

class BookReader:
    def __init__(self):
        self._formats = []

        self._support_all()

    def _support(self, format):
        assert issubclass(format, BookInfo)

        self._formats.append(format)

    def _support_all(self):
        from formats.fb2 import FB2BookInfo
        from formats.epub import EpubBookInfo

        self._support(FB2BookInfo)
        self._support(EpubBookInfo)

    def supports(self, filename):
        return len([ format for format in self._formats if format.supports(filename) ]) > 0

    def info(self, filename):
        book_info = None

        for format in self._formats:
            if format.supports(filename):
                book_info = format(filename)
                break

        return book_info
