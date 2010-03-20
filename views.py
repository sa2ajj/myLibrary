
from django.http import Http404

def bad(request, what):
    raise Http404('"%s" is not a valid path' % what)
