from django.conf.urls.defaults import *

urlpatterns = patterns('myLibrary.web.views',
    (r'^$', 'index'),
    (r'^book$', 'list_books'),
    (r'^book/(?P<id>.+)$', 'show_book'),
    (r'^file/(?P<id>.+)$', 'download_file'),
    (r'^author$', 'list_authors'),
    (r'^author/(?P<id>.+)$', 'show_author'),
    (r'^tag$', 'list_tags'),
    (r'^tag/(?P<id>.+)$', 'show_tag'),
    (r'^series$', 'list_series'),
    (r'^series/(?P<id>.+)$', 'show_series')
)
