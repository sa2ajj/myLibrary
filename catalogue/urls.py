from django.conf.urls.defaults import *

urlpatterns = patterns('myLibrary.catalogue.views',
    (r'^$', 'index'),
)
