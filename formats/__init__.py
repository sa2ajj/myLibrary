
''' base for various book formats '''

from os import stat
from datetime import datetime
from sha import sha

class BookInfoError(Exception):
    ''' exception '''
    pass

BookInfoNotImplemented = BookInfoError('Not implemented')

class BookInfo(object):
    ''' abstract book information class '''

    def __init__(self, path):
        self._path = path
        self._stamp = None

        self._fnhash = None

    @staticmethod
    def format_name():
        ''' human readable format name '''
        raise BookInfoNotImplemented

    @staticmethod
    def supports(filename):
        ''' checks whether a file is supported

        (usually based on file extension)
        '''
        raise BookInfoNotImplemented

    def validate(self):
        ''' reads and validates the book at self._path '''
        raise BookInfoNotImplemented

    @property
    def valid(self):
        ''' tells whether the instance is representing a valid book

        (in other words, whether the properties below would give a valid value
        '''
        raise BookInfoNotImplemented

    @property
    def language(self):
        ''' the book language '''
        raise BookInfoNotImplemented

    @property
    def title(self):
        ''' the book title '''
        raise BookInfoNotImplemented

    @property
    def authors(self):
        ''' list of book authors

        order is important
        '''
        raise BookInfoNotImplemented

    @property
    def series(self):
        ''' list of series the book belong to

        format: [ (<series name>, <series #>), ... ]
        '''
        raise BookInfoNotImplemented

    @property
    def tags(self):
        ''' list of tags for the book '''
        raise BookInfoNotImplemented

    @property
    def mimetype(self):
        ''' mime type for the book's file '''
        raise BookInfoNotImplemented

    @property
    def path(self):
        ''' path to the book's file '''
        return self._path

    @property
    def stamp(self):
        ''' last modified stamp '''
        if self._stamp is None:
            info = stat(self._path)

            self._stamp = datetime.fromtimestamp(info[8])

        return self._stamp

    @property
    def id(self):
        ''' book id

        format: (<id schema>, <id>)
        '''
        if self._fnhash is None:
            self._fnhash = sha(self.path).hexdigest()

        return ('fnhash', self._fnhash)

    @property
    def annotation(self):
        ''' book's annotation '''
        raise BookInfoNotImplemented

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

# vim:ts=4:sw=4:et
