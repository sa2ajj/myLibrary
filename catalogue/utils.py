#

from catalogue.models import BookFormat, Book, Author, BookAuthor, Series, BookSeries, Tag, BookTag

def safe_text(text):
    return text.encode('utf-8')

def print_info(book_info):
    if book_info.valid:
        print 'file:', book_info.path
        print ' title:', safe_text(book_info.title)
        print ' authors:'
        for author in book_info.authors:
            print '  ', safe_text(author)
        print ' lang:', safe_text(book_info.language)
        if book_info.series:
            print ' series:'
            for series, number in book_info.series:
                print '   %s (#%s)' % (safe_text(series), number)
        if book_info.tags:
            print ' tags:'
            for tag in book_info.tags:
                print '  ', safe_text(tag)
    else:
        print '%s is invalid' % book_info.path

def update_book(book_info):
    book_id = book_info.id

    books = Book.objects.filter(uid=book_id[1], uid_scheme=book_id[0])

    mode = 'read'

    if books:
        if books[0].file_stamp < book_info.stamp:
            mode = 'update'
            book = books[0]
        else:
            mode = 'skip'

    if mode in ('read', 'update'):
        print 'update_book:', mode

        book_info.validate()

        if book_info.valid:
            print 'update_book: found a book:', book_info.path, book_info.stamp

            if 1:
                print_info(book_info)

            if mode == 'read':
                format, _ = BookFormat.objects.get_or_create(name=book_info.format_name())
                book = Book(
                    uid=book_id[1],
                    uid_scheme=book_id[0],
                    title=book_info.title,
                    language=book_info.language,
                    file=book_info.path,
                    file_stamp=book_info.stamp,
                    mimetype=book_info.mimetype,
                    format=format,
                    annotation=book_info.annotation
                )
            else:
                # it is assumed that book format does not change
                book.uid=book_id[1]
                book.uid_scheme=book_id[0]
                book.title=book_info.title
                book.language=book_info.language
                book.file=book_info.path
                book.file_stamp=book_info.stamp
                book.mimetype=book_info.mimetype
                book.annotation=book_info.annotation

                for author in book.bookauthor_set.all():
                    author.delete()

                for series in book.bookseries_set.all():
                    series.delete()

                for tag in book.booktag_set.all():
                    tag.delete()

            book.save()

            for position, author in enumerate(book_info.authors):
                db_author, _ = Author.objects.get_or_create(name=author)

                bookauthor = BookAuthor(book=book, author=db_author, position=position+1)
                bookauthor.save()

            for series, number in book_info.series:
                db_series, _ = Series.objects.get_or_create(name=series)

                bookseries = BookSeries(book=book, series=db_series, number=number)
                bookseries.save()

            for tag in book_info.tags:
                db_tag, _ = Tag.objects.get_or_create(name=tag)

                booktag = BookTag(book=book, tag=db_tag)
                booktag.save()
        else:
            print 'update_book: not a valid book at', book_info.path
    elif mode == 'skip':
        print 'update_book: %s already registered and is up to date' % book_info.path
