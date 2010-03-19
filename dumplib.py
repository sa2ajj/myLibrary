#! /usr/bin/python

import os

from formats import scan_dir
from catalogue.utils import print_info

from pprint import pprint

LIB_DIR = '/Downloads/Books'

def main():
    reader = BookReader()

    for info in scan_dir(LIB_DIR, 'fb2'):
        info.validate()
        print_info(info)

if __name__ == '__main__':
    main()
