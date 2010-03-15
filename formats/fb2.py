
import sys

from formats import BookInfo
from formats.utils import parse_xml, get_good_zip, dump

from pprint import pprint

FB2_NS = 'http://www.gribuser.ru/xml/fictionbook/2.0'

ROOT_ELEM = '{%s}FictionBook' % FB2_NS

TITLE_INFO_ELEM = '{%s}title-info' % FB2_NS
TITLE_ELEM = '{%s}book-title' % FB2_NS
TAG_ELEM = '{%s}genre' % FB2_NS
LANG_ELEM = '{%s}lang' % FB2_NS
AUTHOR_ELEM = '{%s}author' % FB2_NS
SERIES_ELEM = '{%s}series' % FB2_NS

DOCUMENT_INFO_ELEM = '{%s}document-info' % FB2_NS
ID_ELEM = '{%s}id' % FB2_NS

PERSON_FIRST_NAME = '{%s}first-name' % FB2_NS
PERSON_MIDDLE_NAME = '{%s}middle-name' % FB2_NS
PERSON_LAST_NAME = '{%s}last-name' % FB2_NS

def strip_text(text):
    if text is None:
        return ''
    else:
        return text.strip()

def person2str(elem):
    ''' convert a FB2 representation of a person to string '''

    name = []

    for child_name in (PERSON_FIRST_NAME, PERSON_MIDDLE_NAME, PERSON_LAST_NAME):
        child = elem.findall('%s' % child_name)

        if child:
            text = strip_text(child[0].text)

            if text:
                name.append(text)

    return ' '.join(name)

def tag2tag(elem):
    return strip_text(elem.text)

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

        if self.supports(self.path):
            self._read()

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

    def _read(self):
        if self.path.endswith('.fb2.zip'):
            archive = get_good_zip(self.path)

            if archive is None:
                print >> sys.stderr, '%s is not a valid zip file' % self.path
                return

            files = archive.namelist()

            if len(files) != 1:     # the .zip file contains several books, fail!
                return

            data = archive.read(files[0])
        else:
            data = open(self.path, 'r').read()

        root = parse_xml(data, True, self.path)

        if root is None:
            print >> sys.stderr, 'Invalid data in %s' % self.path
            return

        if root.tag != ROOT_ELEM:
            print >> sys.stderr, '%s has wrong root element: %s' % (self.path, root.tag)
            return

        title_info = root.find('.//%s' % TITLE_INFO_ELEM)
        if not title_info:
            print >> sys.stderr, 'Could not find title-info for %s' % self.path
            print >> sys.stderr, '  elem:', TITLE_INFO_ELEM
            dump(root, stream=sys.stderr)
            return

        for child in title_info:
            if child.tag == AUTHOR_ELEM:
                self._authors.append(person2str(child))
            elif child.tag == TITLE_ELEM:
                self._title = strip_text(child.text)
            elif child.tag == TAG_ELEM:
                self._tags.append(tag2tag(child))
            elif child.tag == LANG_ELEM:
                self._language = strip_text(child.text)
            elif child.tag == SERIES_ELEM:
                if name in child and child['name']:
                    self._series.append((child['name'], child['number']))

        doc_info = root.find('.//%s' % DOCUMENT_INFO_ELEM)
        if not doc_info:
            print >> sys.stderr, 'Could not find document-info for %s' % self.path
            print >> sys.stderr, '  elem:', DOCUMENT_INFO_ELEM
            # dump(root, stream=sys.stderr)
            return

        # dump(root)

        self._valid = True

# vim:ts=4:sw=4:et
