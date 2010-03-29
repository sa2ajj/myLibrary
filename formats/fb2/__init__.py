
"""BookInfo for a book in FB2 format"""

from formats import BookInfo, BookInfoError

from formats.fb2.reader import read

class FB2BookInfo(BookInfo):
    """BookInfo for a book in FB2 format"""

    def __init__(self, path):
        super(FB2BookInfo, self).__init__(path)

        self._valid = False     # is it valid?

        self._title = None
        self._language = None
        self._authors = []
        self._series = []
        self._tags = []
        self._annotation = None

        self._cover = None

    @classmethod
    def format_name(cls):
        """human readable format name"""

        return 'FB2'

    @classmethod
    def supports(cls, filename):
        """checks whether a file is supported"""

        return filename.endswith('.fb2.zip') or filename.endswith('.fb2')

    @property
    def valid(self):
        """tells whether the instance is representing a valid book"""

        return self._valid

    def _fail_if_not_valid(self):
        """raises an exception if the instances is not representing a valid book"""

        if not self._valid:
            raise BookInfoError('Attempt to get properties for a non-valid book')

    @property
    def language(self):
        """book's language"""

        self._fail_if_not_valid()

        return self._language

    @property
    def title(self):
        """book's title"""

        self._fail_if_not_valid()

        return self._title

    @property
    def authors(self):
        """list of book's authors"""

        self._fail_if_not_valid()

        return self._authors

    @property
    def series(self):
        """list of series the book belongs to"""

        self._fail_if_not_valid()

        return self._series

    @property
    def tags(self):
        """list of book's tags"""

        self._fail_if_not_valid()

        return self._tags

    @property
    def mimetype(self):
        """mime type for the book's file"""

        if not self.supports(self.path):
            raise BookInfoError('Mime-type requested for an unsupported file')

        if self.path.endswith('.fb2.zip'):
            return 'application/fb2+zip'
        elif self.path.endswith('.fb2'):
            return 'application/fb2'

    @property
    def annotation(self):
        """book's annotation"""

        self._fail_if_not_valid()

        return self._annotation

    def validate(self):
        """validates the instance"""

        if not self.supports(self.path):
            return

        result = read(self.path)

        if result is not None:
            for name, value in result.iteritems():
                propname = '_%s' % name

                if propname in self.__dict__:
                    self.__dict__[propname] = value

            self._valid = True

    @property
    def cover(self):
        """book's cover page (as it is)"""

        self._fail_if_not_valid()

        return self._cover

# vim:ts=4:sw=4:et
