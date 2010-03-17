import os

from django.http import HttpResponse, Http404, HttpResponseNotAllowed, HttpResponseServerError
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

# vim:ts=4:sw=4:et
