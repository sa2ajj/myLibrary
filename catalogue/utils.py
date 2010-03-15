#

def safe_text(text):
    return text.encode('utf-8')

def print_info(book_info):
    if book_info.valid:
        print ' title:', safe_text(book_info.title)
        print ' authors:'
        for author in book_info.authors:
            print '  ', safe_text(author)
        print ' lang:', safe_text(book_info.language)
        print ' series:'
        for series in book_info.series:
            print '  ', safe_text(series)
        print ' tags:'
        for tag in book_info.tags:
            print '  ', safe_text(tag)

def update_book(book_info):
    if book_info.valid:
        print 'update_book: found a book:', book_info.path, book_info.stamp
        print_info(book_info)
    else:
        print 'update_book: not a valid book at', book_info.path
