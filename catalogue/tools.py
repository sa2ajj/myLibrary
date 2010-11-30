#

import logging
LOG = logging.getLogger(__name__)

from catalogue.models import BookFormat, Book, Author, BookAuthor, Series, \
                             BookSeries, Tag, BookTag
def _safe_text(text):
    return text.encode('utf-8')

def print_info(book_info):
    if book_info.valid:
        print 'file:', book_info.path
        print ' title:', _safe_text(book_info.title)
        print ' authors:'
        for author in book_info.authors:
            print '  ', _safe_text(author)
        print ' lang:', _safe_text(book_info.language)
        if book_info.series:
            print ' series:'
            for series, number in book_info.series:
                print '   %s (#%s)' % (_safe_text(series), number)
        if book_info.tags:
            print ' tags:'
            for tag in book_info.tags:
                print '  ', _safe_text(tag)
    else:
        print '%s is invalid' % book_info.path

def update_book(book_info):
    book_id = book_info.book_id

    books = Book.objects.filter(uid=book_id[1], uid_scheme=book_id[0])

    mode = 'read'

    if books:
        if books[0].file_stamp < book_info.stamp:
            mode = 'update'
            book = books[0]
        else:
            mode = 'skip'

    if mode in ('read', 'update'):
        LOG.info('update_book:', mode)

        book_info.validate()

        if book_info.valid:
            LOG.info('update_book: found a book: %s, %s', book_info.path,
                                                          book_info.stamp)
            if 1:
                print_info(book_info)

            if mode == 'read':
                fmt, _ = BookFormat.objects.get_or_create(name=book_info.format_name())
                book = Book(
                    uid=book_id[1],
                    uid_scheme=book_id[0],
                    title=book_info.title,
                    language=book_info.language,
                    file=book_info.path,
                    file_stamp=book_info.stamp,
                    mimetype=book_info.mimetype,
                    format=fmt,
                    annotation=book_info.annotation
                )
            else:
                # it is assumed that book format does not change
                book.uid = book_id[1]
                book.uid_scheme = book_id[0]
                book.title = book_info.title
                book.language = book_info.language
                book.file = book_info.path
                book.file_stamp = book_info.stamp
                book.mimetype = book_info.mimetype
                book.annotation = book_info.annotation

                book.authors.clear()
                book.series.clear()
                book.tags.clear()

            book.save()

            for position, author in enumerate(book_info.authors, 1):
                db_author, _ = Author.objects.get_or_create(name=author)

                bookauthor = BookAuthor(book=book, author=db_author,
                                        position=position)
                bookauthor.save()

            for series, number in book_info.series:
                db_series, _ = Series.objects.get_or_create(name=series)

                bookseries = BookSeries(book=book, series=db_series,
                                        number=number)
                bookseries.save()

            for tag in book_info.tags:
                if '/' in tag:
                    db_tag = None

                    for name in [x.strip() for x in tag.split('/')]:
                        db_tag, _ = Tag.objects.get_or_create(name=name,
                                                              parent=db_tag)
                else:
                    db_tag, _ = Tag.objects.get_or_create(name=tag)

                booktag = BookTag(book=book, tag=db_tag)
                booktag.save()
        else:
            LOG.error('update_book: not a valid book at', book_info.path)
    elif mode == 'skip':
        LOG.warn('update_book: %s already registered and is up to date',
                 book_info.path)
