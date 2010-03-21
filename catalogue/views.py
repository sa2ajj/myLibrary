from django.http import HttpResponse

from catalogue.feeds import Feed, FeedItemFeed

def index(request):
    feed = Feed(request.build_absolute_uri(), 'Index for the catalogue')

    return HttpResponse(unicode(feed), mimetype=feed.mimetype)
