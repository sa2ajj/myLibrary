import os

from django.http import HttpResponse, Http404, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import get_object_or_404, render_to_response

from catalogue.models import Book, Author, Tag, Series

def _validate_id(id):
    try:
        id = int(id)
    except ValueError:
        raise Http404, 'Invalid book id'

    return id

def index(request):
    return render_to_response('home.html')

def list_books(request):
    books = Book.objects.order_by('title')

    return render_to_response('books.html', dict(books=books))

def show_book(request, id):
    id = _validate_id(id)

    book = get_object_or_404(Book, id=id)

    authors = [ x.author for x in book.bookauthor_set.order_by('position') ]
    tags = [ x.tag for x in book.booktag_set.order_by('tag__name') ]

    return render_to_response('book.html', dict(book=book, authors=authors, tags=tags))

def download_file(request, id):
    id = _validate_id(id)

    if request.method != 'GET':
        return HttpResponseNotAllowed([ 'GET' ])

    book = get_object_or_404(Book, id=id)

    try:
        content = open(book.file, 'rb')
    except IOError:
        return HttpResponseServerError('Cannot open the requested file')

    data = content.read()
    content.close()

    response = HttpResponse(mimetype=book.mimetype)
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(book.file)
    response["Content-Length"] = len(data)

    response.write(data)

    return response

def list_authors(request):
    authors = Author.objects.order_by('name')

    return render_to_response('authors.html', dict(authors=authors))

def show_author(request, id):
    id = _validate_id(id)

    author = get_object_or_404(Author, id=id)

    books = [ x.book for x in author.bookauthor_set.order_by('book__title') ]

    return render_to_response('author.html', dict(author=author, books=books))

def list_tags(request):

    not_tagged = Book.objects.filter(booktag=None)

    tags = [
        (tag.id, tag.name, tag.booktag_set.count(), Tag.objects.filter(parent=tag).count()) \
            for tag in Tag.objects.filter(parent=None).order_by('name')
    ]

    tags.insert(0, ('none', '<no tag>', len(not_tagged), 0))

    return render_to_response('tags.html', dict(tags=tags))

def show_tag(request, id):
    if id == 'none':
        tag = '<no tag>'
        subtags, tag_path = [], []
        books = Book.objects.filter(booktag=None)
    else:
        id = _validate_id(id)

        tag = get_object_or_404(Tag, id=id)

        tag_path = []
        parent = tag.parent

        while parent is not None:
            tag_path.insert(0, parent)
            parent = parent.parent

        subtags = [
            (x.id, x.name, x.booktag_set.count(), Tag.objects.filter(parent=x).count()) \
                for x in Tag.objects.filter(parent=tag).order_by('name')
        ]
        books = [ x.book for x in tag.booktag_set.order_by('book__title') ]

    return render_to_response('tag.html', dict(tag=tag, subtags=subtags, books=books, tag_path=tag_path))

def list_series(request):

    series = Series.objects.order_by('name')

    return render_to_response('all-series.html', dict(series=series))

def show_series(request, id):
    id = _validate_id(id)

    series = Series.objects.get(id=id)

    books = [ (x.number, x.book) for x in series.bookseries_set.order_by('number') ]

    return render_to_response('series.html', dict(series=series, books=books))

# vim:ts=4:sw=4:et
