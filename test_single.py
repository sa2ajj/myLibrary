#! /usr/bin/python -tt
# -*- coding: utf-8 -*-

from formats.fb2 import FB2BookInfo
from formats.epub import EpubBookInfo
from catalogue.tools import print_info

for filename in (
        '/Downloads/Books/other/Books/Vadim Panov/9- Кафедра странников/panov_tayiniyyi_gorod_9_kafedra_strannikov.fb2.zip',
    ):
    book = FB2BookInfo(filename)

    print 'Processing:', book.path
    print '  last modified:', book.stamp
    print '  id:', book.id

    book.validate()

    if book.valid:
        print_info(book)
    else:
        print 'Invalid book'

for filename in (
        '/Downloads/Books/epub/MakingThingsHappen.epub',
        '/Downloads/Books/Scalzi,_John_-_Old_Man\'s_War_04_-_Zoe\'s_Tale.epub',
        '/Downloads/Books/Carver - Strange Attractors.epub'
    ):
    book = EpubBookInfo(filename)

    print 'Processing:', book.path
    print '  last modified:', book.stamp
    print '  id:', book.id

    book.validate()

    if book.valid:
        print_info(book)
    else:
        print 'Invalid book'
