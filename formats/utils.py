
''' A number of commonly used functions '''

import sys
import zipfile

from xml.etree import ElementTree as ET

from traceback import print_exc

def get_good_zip(zipname, test=False):
    ''' a helper function that returns an instance of ZipFile for a good zip file '''

    try:
        archive = zipfile.ZipFile(zipname)
    except zipfile.BadZipfile:
        print >> sys.stderr, '%s is not a zip file' % zipname
        return

    if test and archive.testzip():
        print >> sys.stderr, '%s is broken' % zipname
        return

    return archive

def parse_xml(data, info=False, label=None):
    ''' parses provided XML string using ElementTree '''

    try:
        result = ET.fromstring(data)
    except:
        # TODO: try to find a way to catch the right exception only
        if info:
            print_exc()
            if label:
                print >> sys.stderr, 'Label:', label
            print >> sys.stderr, 'parse_xml: %s: %s' % (type(data), data)

        result = None

    return result

def dump(elem, indent=0, stream=sys.stdout):
    ''' pretty dumps an ElementTree '''

    if elem is None:
        print >> stream, 'OOPS: no elem to dump'
        return

    if elem.text:
        text = ' text: %s' % repr(elem.text)
    else:
        text = ''

    print >> stream, '%sdump: %s %s%s' % (' '*indent, elem.tag, elem.attrib, text)

    for child in elem:
        dump(child, indent+2, stream)

# vim:ts=4:sw=4:et
