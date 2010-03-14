#

def update_book(book_info):
    if book_info.valid:
        print 'update_book: found a book:', book_info.path, book_info.stamp, book_info
    else:
        print 'update_book: not a valid book at', book_info.path
