
import sys
import zipfile

from xml.etree import ElementTree as ET

from traceback import print_exc

def get_good_zip(zipname):
    ''' a helper function that returns an instance of ZipFile for a good zip file '''

    try:
        archive = zipfile.ZipFile(zipname)
    except zipfile.BadZipfile:
        print >> sys.stderr, '%s is not a zip file' % zipname
        return

    if archive.testzip():
        print >> sys.stderr, '%s is broken' % zipname
        return

    return archive

def parse_xml(data, dump=False):
    try:
        result = ET.fromstring(data).getroot()
    except:
        # TODO: try to find a way to catch the right exception only
        if dump:
            print_exc()
            print >> sys.stderr, 'parse_xml: %s: %s' % (type(data), data)

        result = None

    return result
