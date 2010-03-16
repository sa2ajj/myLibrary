
import sys

from formats import BookInfo, BookInfoError
from formats.epub.reader import read

class EpubBookInfo(BookInfo):
    def __init__(self, path):
        super(EpubBookInfo, self).__init__(path)

        self._valid = False     # is it valid?

        self._title = None
        self._language = None
        self._authors = []
        self._series = []
        self._tags = []
        self._annotation = None

    @staticmethod
    def format_name():
        return 'ePub'

    @staticmethod
    def supports(filename):
        return filename.endswith('.epub')

    @property
    def valid(self):
        return self._valid

    def _fail_if_not_valid(self):
        if not self._valid:
            raise BookInfoError('Attempt to get properties for a non-valid book')

    @property
    def language(self):
        self._fail_if_not_valid()

        return self._language

    @property
    def title(self):
        self._fail_if_not_valid()

        return self._title

    @property
    def authors(self):
        self._fail_if_not_valid()

        return self._authors

    @property
    def series(self):
        self._fail_if_not_valid()

        return self._series

    @property
    def tags(self):
        self._fail_if_not_valid()

        return self._tags

    @property
    def annotation(self):
        self._fail_if_not_valid()

        return self._annotation

    @property
    def mimetype(self):
        if not self.supports(self.path):
            raise BookInfoError('Mime-type requested for an unsupported file')

        return 'application/epub+zip'

    def validate(self):
        if not self.supports(self.path):
            return

        result = read(self.path)

        if result is not None:
            for name, value in result.iteritems():
                propname = '_%s' % name

                if propname in self.__dict__:
                    self.__dict__[propname] = value

            self._valid = True

# vim:ts=4:sw=4:et
