
import sys

from formats.utils import parse_xml, get_good_zip, dump

FB2_NS = 'http://www.gribuser.ru/xml/fictionbook/2.0'

ROOT_ELEM = '{%s}FictionBook' % FB2_NS

TITLE_INFO_ELEM = '{%s}title-info' % FB2_NS
TITLE_ELEM = '{%s}book-title' % FB2_NS
TAG_ELEM = '{%s}genre' % FB2_NS
LANG_ELEM = '{%s}lang' % FB2_NS
AUTHOR_ELEM = '{%s}author' % FB2_NS
SERIES_ELEM = '{%s}sequence' % FB2_NS

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

def read(path):
    if path.endswith('.fb2.zip'):
        archive = get_good_zip(path)

        if archive is None:
            print >> sys.stderr, '%s is not a valid zip file' % path
            return

        files = archive.namelist()

        if len(files) != 1:     # the .zip file contains several books, fail!
            return

        data = archive.read(files[0])
    else:
        data = open(path, 'r').read()

    root = parse_xml(data, True, path)

    if root is None:
        print >> sys.stderr, 'Invalid data in %s' % path
        return

    if root.tag != ROOT_ELEM:
        print >> sys.stderr, '%s has wrong root element: %s' % (path, root.tag)
        return

    if 0:
        dump(root)

    title_info = root.find('.//%s' % TITLE_INFO_ELEM)
    if not title_info:
        print >> sys.stderr, 'Could not find title-info for %s' % path
        print >> sys.stderr, '  elem:', TITLE_INFO_ELEM
        dump(root, stream=sys.stderr)
        return

    title = None
    language = None
    authors = []
    series = []
    tags = []
    annotation = None

    for child in title_info:
        if child.tag == AUTHOR_ELEM:
            authors.append(person2str(child))
        elif child.tag == TITLE_ELEM:
            title = strip_text(child.text)
        elif child.tag == TAG_ELEM:
            tags.append(tag2tag(child))
        elif child.tag == LANG_ELEM:
            language = strip_text(child.text)
        elif child.tag == SERIES_ELEM:
            if 'name' in child.attrib and child.attrib['name']:
                series.append((child.attrib['name'], child.attrib['number']))

    return {
        'title': title,
        'language': language,
        'authors': authors,
        'series': series,
        'tags': tags,
        'annotation': annotation,
    }

# vim:ts=4:sw=4:et
