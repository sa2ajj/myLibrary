#! /usr/bin/python

import os

from formats import scan_dir
from catalogue.utils import update_book

from pprint import pprint

LIB_DIR = '/Downloads/Books'

def main():
    for info in scan_dir(LIB_DIR, 'fb2'):
        update_book(info)

if __name__ == '__main__':
    main()
