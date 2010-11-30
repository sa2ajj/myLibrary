"""FB2 file reader"""

import logging
LOG = logging.getLogger(__name__)

import sys

from base64 import decodestring

from cStringIO import StringIO

from PIL import Image

from formats.utils import get_good_zip
from formats.fb2.genres import normalize_tag

from xmlutils import parse_xml, dump

FB2_NS = 'http://www.gribuser.ru/xml/fictionbook/2.0'
XLINK_NS = 'http://www.w3.org/1999/xlink'

XLINK_HREF = '{%s}href' % XLINK_NS

ROOT_ELEM = '{%s}FictionBook' % FB2_NS

TITLE_INFO_ELEM = '{%s}title-info' % FB2_NS
TITLE_ELEM = '{%s}book-title' % FB2_NS
TAG_ELEM = '{%s}genre' % FB2_NS
LANG_ELEM = '{%s}lang' % FB2_NS
AUTHOR_ELEM = '{%s}author' % FB2_NS
SERIES_ELEM = '{%s}sequence' % FB2_NS
COVER_ELEM = '{%s}coverpage' % FB2_NS
IMAGE_ELEM = '{%s}image' % FB2_NS
BINARY_ELEM = '{%s}binary' % FB2_NS

DOCUMENT_INFO_ELEM = '{%s}document-info' % FB2_NS
ID_ELEM = '{%s}id' % FB2_NS

PERSON_FIRST_NAME = '{%s}first-name' % FB2_NS
PERSON_MIDDLE_NAME = '{%s}middle-name' % FB2_NS
PERSON_LAST_NAME = '{%s}last-name' % FB2_NS

def strip_text(text):
    """return normalized text for an element.text"""

    if text is None:
        return ''
    else:
        return text.strip()

def person2str(elem):
    """convert a FB2 representation of a person to string"""

    name = []

    for child_name in (PERSON_FIRST_NAME, PERSON_MIDDLE_NAME, PERSON_LAST_NAME):
        child = elem.findall('%s' % child_name)

        if child:
            text = strip_text(child[0].text)

            if text:
                name.append(text)

    return ' '.join(name)

def tag2tag(elem):
    """produce tag on based element's text value"""

    return strip_text(elem.text)

def normalize_tags(tags):
    """return a list of tag hierarchies based on genres list"""

    return list(set([ normalize_tag(x) for x in tags ]))

def read_fb2_file(path):
    """reads fb2/fb2.zip file and returns xml internal representation"""

    if path.endswith('.fb2.zip'):
        archive = get_good_zip(path)

        if archive is None:
            LOG.error('%s is not a valid zip file', path)
            return

        files = archive.namelist()

        if len(files) != 1:     # the .zip file contains several books, fail!
            return

        data = archive.read(files[0])
    else:
        data = open(path, 'r').read()

    return data

def get_root(data, path):
    """parses supplied data and returns its root element"""

    root = parse_xml(data, True, path)

    if root is None:
        LOG.error('Invalid data in %s', path)
        return

    if root.tag != ROOT_ELEM:
        LOG.error('%s has wrong root element: %s (expected %s)',
                  path, root.tag, ROOT_ELEM)
        return

    if 0:
        dump(root)

    return root

def read(path):
    """read a FB2 file and return extracted meta-information"""

    LOG.debug("reading %s", path)

    data = read_fb2_file(path)

    if data is None:
        return

    root = get_root(data, path)

    title_info = root.find('.//%s' % TITLE_INFO_ELEM)
    if not title_info:
        LOG.error('Could not find title-info for %s', path)
        LOG.error('  elem:', TITLE_INFO_ELEM)
        dump(root, stream=sys.stderr)
        return

    title = None
    language = None
    authors = []
    series = []
    tags = []
    annotation = None
    cover = None

    for child in title_info:
        if child.tag == AUTHOR_ELEM:
            authors.append(person2str(child))
        elif child.tag == TITLE_ELEM:
            title = strip_text(child.text)
        elif child.tag == TAG_ELEM:
            tag = tag2tag(child)
            if tag:     # add only non-empty tags
                tags.append(tag)
        elif child.tag == LANG_ELEM:
            language = strip_text(child.text)
        elif child.tag == SERIES_ELEM:
            if 'name' in child.attrib and child.attrib['name'] \
                                      and child.attrib.get('number', 0):
                series.append((child.attrib['name'], child.attrib['number']))
        elif child.tag == COVER_ELEM:
            if len(child) and \
               child[0].tag == IMAGE_ELEM and XLINK_HREF in child[0].attrib:
                value = child[0].attrib[XLINK_HREF]

                if value[0] == '#':
                    value = value[1:]

                binary = [binary for binary in root.findall(BINARY_ELEM) \
                                 if 'id' in binary.attrib and \
                                            binary.attrib['id'] == value]
                if len(binary) == 1:
                    cover = Image.open(StringIO(decodestring(binary[0].text)))

    return {
        'title': title,
        'language': language,
        'authors': authors,
        'series': series,
        'tags': normalize_tags(tags),
        'annotation': annotation,
        'cover': cover,
    }

# vim:ts=4:sw=4:et
