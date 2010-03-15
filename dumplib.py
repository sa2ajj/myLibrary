#! /usr/bin/python

import os

from formats import BookReader
from catalogue.utils import print_info

from pprint import pprint

LIB_DIR = '/Downloads/Books'

def main():
    reader = BookReader()

    for path, _, filenames in os.walk(LIB_DIR):
        for filename in filenames:
            fullpath = os.path.join(path, filename)

            if reader.supports(fullpath):
                info = reader.info(fullpath)
                info.validate()
                print_info(info)

if __name__ == '__main__':
    main()
