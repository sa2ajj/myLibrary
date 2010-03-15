
from formats import BookInfo

from formats.fb2.reader import read

class FB2BookInfo(BookInfo):
    def __init__(self, path):
        super(FB2BookInfo, self).__init__(path)

        self._valid = False     # is it valid?

        self._title = None
        self._language = None
        self._authors = []
        self._series = []
        self._tags = []
        self._annotation = None

    @staticmethod
    def format_name():
        return 'FB2'

    @staticmethod
    def supports(filename):
        return filename.endswith('.fb2.zip') or filename.endswith('.fb2')

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