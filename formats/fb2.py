
from formats import BookInfo

class FB2BookInfo(BookInfo):
    @staticmethod
    def format_name():
        return 'FB2'

    @staticmethod
    def supports(filename):
        return filename.endswith('.fb2.zip') or filename.endswith('.fb2')

    @property
    def valid(self):
        return False

    @property
    def title(self):
        return 'FB2: title'

    @property
    def authors(self):
        return 'FB2: authors'

# vim:ts=4:sw=4:et
