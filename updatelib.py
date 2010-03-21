#! /usr/bin/python

"""An utility to scan directories for books

It can work in two modes:
    * update the library (default)
    * display the information about found books
"""

from formats import scan_dir
from catalogue.utils import update_book

LIB_DIR = '/Downloads/Books'

def main():
    """main worker"""

    for info in scan_dir(LIB_DIR, 'fb2'):
        update_book(info)

if __name__ == '__main__':
    main()
