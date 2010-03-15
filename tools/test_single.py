#! /usr/bin/python -tt
# -*- coding: utf-8 -*-

from formats.fb2 import FB2BookInfo
from catalogue.utils import print_info

book = FB2BookInfo('/Downloads/Books/other/Books/Vadim Panov/9- Кафедра странников/panov_tayiniyyi_gorod_9_kafedra_strannikov.fb2.zip')

print 'Processing:', book.path
print '  last modified:', book.stamp
print '  id:', book.id

book.validate()

if book.valid:
    print_info(book)
else:
    print 'Invalid book'
