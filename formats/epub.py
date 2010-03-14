
from formats import BookInfo

class EpubBookInfo(BookInfo):
    @staticmethod
    def format_name():
        return 'ePub'

    @staticmethod
    def supports(filename):
        return filename.endswith('.epub')

    @property
    def valid(self):
        return False

    @property
    def title(self):
        return 'ePub: title'

    @property
    def authors(self):
        return 'ePub: authors'
