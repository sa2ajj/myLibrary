from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response

from catalogue.models import Book, BookAuthor, BookTag

def _validate_id(id):
    try:
        id = int(id)
    except ValueError:
        raise Http404, 'Invalid book id'

    return id

def index(request):
    return HttpResponse('Index for the catalogue (web)')

def show_book(request, id):
    id = _validate_id(id)

    book = get_object_or_404(Book, id=id)

    authors = [ x.author for x in BookAuthor.objects.filter(book=book).order_by('position') ]
    tags = [ x.tag for x in BookTag.objects.filter(book=book).order_by('tag__name') ]

    return render_to_response('book.html', dict(book=book, authors=authors, tags=tags))

# vim:ts=4:sw=4:et
