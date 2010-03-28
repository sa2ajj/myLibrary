from django.http import HttpResponse

from catalogue.feeds import Feed, FeedItemFeed

def index(request):
    """Root catalogue"""

    get_uri = lambda x=None: request.build_absolute_uri(x)

    feed = Feed(get_uri(), 'Index for the catalogue')

    feed.add(FeedItemFeed('Books', get_uri('books')))
    feed.add(FeedItemFeed('Authors', get_uri('authors')))
    feed.add(FeedItemFeed('Tags', get_uri('tags')))
    feed.add(FeedItemFeed('Series', get_uri('series')))
    feed.add(FeedItemFeed('New Books', get_uri('new')))

    return HttpResponse(feed.xml(), mimetype=feed.mimetype)

# vim:ts=4:sw=4:et
