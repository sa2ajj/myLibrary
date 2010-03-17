import os

from django.http import HttpResponse, Http404, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import get_object_or_404, render_to_response

from catalogue.models import Book, Author

def _validate_id(id):
    try:
        id = int(id)
    except ValueError:
        raise Http404, 'Invalid book id'

    return id

def index(request):
    return HttpResponse('Index for the catalogue (web)')

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

def show_author(request, id):
    id = _validate_id(id)

    author = get_object_or_404(Author, id=id)

    books = [ x.book for x in author.bookauthor_set.order_by('book__title') ]

    return render_to_response('author.html', dict(author=author, books=books))

# vim:ts=4:sw=4:et
