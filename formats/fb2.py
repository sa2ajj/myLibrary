
from formats import BookInfo

class FB2BookInfo(BookInfo):
    @staticmethod
    def supports(filename):
        return filename.endswith('.fb2.zip')

    @property
    def title(self):
        return 'FB2: title'

    @property
    def authors(self):
        return 'FB2: authors'

