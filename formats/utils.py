
''' A number of commonly used functions '''

import sys
import zipfile

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

# vim:ts=4:sw=4:et
