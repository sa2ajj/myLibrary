
from formats import BookInfo

class EpubBookInfo(BookInfo):
    @staticmethod
    def supports(filename):
        return filename.endswith('.epub')

    @property
    def title(self):
        return 'ePub: title'

    @property
    def authors(self):
        return 'ePub: authors'
