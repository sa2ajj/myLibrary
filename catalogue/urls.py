from django.conf.urls.defaults import patterns

urlpatterns = patterns('myLibrary.catalogue.views',
    (r'^$', 'index'),
    # (r'^book$', 'list_books'),
    # (r'^book/(?P<id>.+)$', 'show_book'),
    # (r'^author$', 'list_authors'),
    # (r'^author/(?P<id>.+)$', 'show_author'),
    # (r'^tag$', 'list_tags'),
    # (r'^tag/(?P<id>.+)$', 'show_tag'),
    # (r'^series$', 'list_series'),
    # (r'^series/(?P<id>.+)$', 'show_series')
)

# vim:ts=4:sw=4:et
