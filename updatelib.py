#! /usr/bin/python

"""An utility to scan directories for books

It can work in two modes:
    * update the library (default)
    * display the information about found books
"""

from optparse import OptionParser

from formats import scan_dir
from catalogue.utils import update_book, print_info

DEFAULT_FORMATS = [ 'fb2' ]

def main():
    """main worker"""

    parser = OptionParser()

    parser.add_option('-p', '--print-only', action='store_true', dest='show', default=False)
    parser.add_option('-f', '--format', action='append', dest='formats', default=[])

    options, dirs = parser.parse_args()

    if not options.formats:
        options.formats = DEFAULT_FORMATS

    for dirname in dirs:
        for info in scan_dir(dirname, *options.formats):
            if options.show:
                info.validate()
                print_info(info)
            else:
                update_book(info)

if __name__ == '__main__':
    main()
