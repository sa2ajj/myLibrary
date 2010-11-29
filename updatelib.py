#! /usr/bin/python

"""An utility to scan directories for books

It can work in two modes:
    * update the library (default)
    * display the information about found books
"""

import logging
LOG = logging.getLogger(__name__)

import sys, os

sys.path.insert(0, os.path.join(os.getcwd(), '..'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'myLibrary.settings'

from optparse import OptionParser

from formats import scan_dir
from catalogue.tools import update_book, print_info

DEFAULT_FORMATS = ['fb2']

def main():
    """main worker"""

    logging.basicConfig()

    parser = OptionParser(usage='%prog [options] <dir> [<dir>...]')

    parser.add_option('-p', '--print-only', action='store_true', dest='show',
                      default=False, help='do not update the database')
    parser.add_option('-f', '--format', action='append', dest='formats',
                      help='format to consider', default=[], metavar='FORMAT')
    parser.add_option('--debug', action='store_true', dest='debug',
                      help='enable debug output')
    options, dirs = parser.parse_args()

    if options.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    if not options.formats:
        options.formats = DEFAULT_FORMATS

    for dirname in [os.path.expanduser(x) for x in dirs]:
        for info in scan_dir(dirname, *options.formats):
            if options.show:
                info.validate()
                print_info(info)
            else:
                update_book(info)

if __name__ == '__main__':
    main()
