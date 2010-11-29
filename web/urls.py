from django.conf.urls.defaults import patterns

urlpatterns = patterns('myLibrary.web.views',
    (r'^$', 'index'),
    (r'^book$', 'list_books'),
    (r'^book/(?P<book_id>.+)$', 'show_book'),
    (r'^file/(?P<file_id>.+)$', 'download_file'),
    (r'^author$', 'list_authors'),
    (r'^author/(?P<author_id>.+)$', 'show_author'),
    (r'^tag$', 'list_tags'),
    (r'^tag/(?P<tag_id>.+)$', 'show_tag'),
    (r'^series$', 'list_series'),
    (r'^series/(?P<series_id>.+)$', 'show_series')
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^about$', 'direct_to_template', dict(template='about.html')),
    (r'^feedback$', 'direct_to_template', dict(template='feedback.html')),
)

# vim:ts=4:sw=4:et
