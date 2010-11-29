
"""base for various book formats"""

import os
from datetime import datetime
from sha import sha

from PIL import Image

__all__ = [ 'BookInfoError', 'BookInfo', 'BookReader' ]

class BookInfoError(Exception):
    """exception"""
    pass

THUMBNAIL_SIZE = (66, 90)

class BookInfo(object):
    """abstract book information class"""

    def __init__(self, path):
        self._path = path
        self._stamp = None

        self._fnhash = None

        self._thumbnail = None

    @classmethod
    def format_name(cls):
        """human readable format name"""
        raise NotImplementedError, 'format_name is not defined in %s' % cls.__name__

    @classmethod
    def supports(cls, filename):
        """checks whether a file is supported

        (usually based on file extension)
        """
        raise NotImplementedError, 'supports is not defined in %s' % cls.__name__

    def validate(self):
        """reads and validates the book at self._path"""
        raise NotImplementedError, 'supports is not defined in %s' % self.__class__.__name__

    @property
    def valid(self):
        """tells whether the instance is representing a valid book

        (in other words, whether the properties below would give a valid value
        """
        raise NotImplementedError, 'valid is not defined in %s' % self.__class__.__name__

    @property
    def language(self):
        """the book language"""
        raise NotImplementedError, 'language is not defined in %s' % self.__class__.__name__

    @property
    def title(self):
        """the book title"""
        raise NotImplementedError, 'title is not defined in %s' % self.__class__.__name__

    @property
    def authors(self):
        """list of book authors

        order is important
        """
        raise NotImplementedError, 'authors is not defined in %s' % self.__class__.__name__

    @property
    def series(self):
        """list of series the book belong to

        format: [ (<series name>, <series #>), ... ]
        """
        raise NotImplementedError, 'series is not defined in %s' % self.__class__.__name__

    @property
    def tags(self):
        """list of tags for the book"""
        raise NotImplementedError, 'tags is not defined in %s' % self.__class__.__name__

    @property
    def mimetype(self):
        """mime type for the book's file"""
        raise NotImplementedError, 'mimetype is not defined in %s' % self.__class__.__name__

    @property
    def path(self):
        """path to the book's file"""
        return self._path

    @property
    def stamp(self):
        """last modified stamp"""
        if self._stamp is None:
            info = os.stat(self._path)

            self._stamp = datetime.fromtimestamp(info[8])

        return self._stamp

    @property
    def book_id(self):
        """book id

        format: (<id schema>, <id>)
        """
        if self._fnhash is None:
            self._fnhash = sha(self.path).hexdigest()

        return ('fnhash', self._fnhash)

    @property
    def annotation(self):
        """book's annotation"""
        raise NotImplementedError, 'annotation is not defined in %s' % self.__class__.__name__

    @property
    def cover(self):
        """book's cover page (as it is)"""
        raise NotImplementedError, 'cover is not defined in %s' % self.__class__.__name__

    @property
    def thumbnail(self):
        """book's cover page thumbnail"""

        if self._thumbnail is None:
            cover = self.cover()

            if cover is not None:
                self._thumbnail = cover.resize(THUMBNAIL_SIZE, Image.ANTIALIAS)

        return self._thumbnail

def scan_dir(dirname, *formats):
    """
    scan the specified directory for books in the specified formats
    """

    from formats.fb2 import FB2BookInfo
    from formats.epub import EpubBookInfo

    known_formats = [ FB2BookInfo, EpubBookInfo ]

    if not formats:
        formats = [x.format_name().lower() for x in known_formats]

    supported = [x for x in known_formats if x.format_name().lower() in formats]

    for path, _, filenames in os.walk(dirname):
        for filename in filenames:
            book_info = None

            for format in supported:
                if format.supports(filename):
                    book_info = format
                    break

            if book_info is not None:
                fullpath = os.path.join(path, filename)
                yield book_info(fullpath)

# vim:ts=4:sw=4:et
