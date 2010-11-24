"""web views"""

import os

from django.http import HttpResponse, Http404, HttpResponseNotAllowed, \
                        HttpResponseServerError
from django.shortcuts import get_object_or_404, render_to_response

from catalogue.models import Book, Author, Tag, Series

ATTACHMENT = 'attachment; filename=%s'

def _validate_id(value):
    """check if the provided id is a number"""

    try:
        result = int(value)
    except ValueError:
        raise Http404, 'Invalid book id'

    return result

def index(request_):
    """home view"""

    return render_to_response('home.html')

def list_books(request_):
    """list registered books"""

    books = Book.objects.order_by('title')

    return render_to_response('books.html', dict(books=books))

def show_book(request_, book_id):
    """show particular book"""

    book_id = _validate_id(book_id)

    book = get_object_or_404(Book, id=book_id)

    authors = [x.author for x in book.bookauthor_set.order_by('position')]
    tags = [x.tag for x in book.booktag_set.order_by('tag__name')]

    return render_to_response('book.html', dict(book=book, authors=authors,
                                                tags=tags))

def download_file(request, file_id):
    """download a file"""

    file_id = _validate_id(file_id)

    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    book = get_object_or_404(Book, id=file_id)

    try:
        content = open(book.file, 'rb')
    except IOError:
        return HttpResponseServerError('Cannot open the requested file')

    data = content.read()
    content.close()

    response = HttpResponse(mimetype=book.mimetype)
    response['Content-Disposition'] = ATTACHMENT % os.path.basename(book.file)
    response["Content-Length"] = len(data)

    response.write(data)

    return response

def list_authors(request_):
    """list known authors"""

    authors = Author.objects.order_by('name')

    return render_to_response('authors.html', dict(authors=authors))

def show_author(request_, author_id):
    """show particular author"""

    author = get_object_or_404(Author, id=_validate_id(author_id))

    books = [x.book for x in author.bookauthor_set.order_by('book__title')]

    return render_to_response('author.html', dict(author=author, books=books))

def list_tags(request_):
    """list registered tags"""

    not_tagged = Book.objects.filter(booktag=None)

    tags = [(tag.id, tag.name, tag.booktag_set.count(),
             Tag.objects.filter(parent=tag).count()) for tag \
                in Tag.objects.filter(parent=None).order_by('name')]

    tags.insert(0, ('none', '<no tag>', len(not_tagged), 0))

    return render_to_response('tags.html', dict(tags=tags))

def show_tag(request_, tag_id):
    """show particular tag"""

    if tag_id == 'none':
        tag = '<no tag>'
        subtags, tag_path = [], []
        books = Book.objects.filter(booktag=None)
    else:
        tag = get_object_or_404(Tag, id=_validate_id(tag_id))

        tag_path = []
        parent = tag.parent

        while parent is not None:
            tag_path.insert(0, parent)
            parent = parent.parent

        subtags = [(x.id, x.name, x.booktag_set.count(),
                    Tag.objects.filter(parent=x).count()) for x \
                        in Tag.objects.filter(parent=tag).order_by('name')]
        books = [x.book for x in tag.booktag_set.order_by('book__title')]

    return render_to_response('tag.html', dict(tag=tag, subtags=subtags,
                                               books=books, tag_path=tag_path))
def list_series(request_):
    """list available series"""

    series = Series.objects.order_by('name')

    return render_to_response('all-series.html', dict(series=series))

def show_series(request_, series_id):
    """show particular series"""

    series = Series.objects.get(id=_validate_id(series_id))

    books = [(x.number, x.book) for x in \
                series.bookseries_set.order_by('number')]
    return render_to_response('series.html', dict(series=series, books=books))

# vim:ts=4:sw=4:et
