from django.conf.urls.defaults import *

urlpatterns = patterns('myLibrary.web.views',
    (r'^$', 'index'),
    (r'^book/(?P<id>.+)$', 'show_book')
)
