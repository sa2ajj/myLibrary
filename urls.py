from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^catalogue/', include('myLibrary.catalogue.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),

    (r'^openid/$', 'django_openidconsumer.views.begin', { 'sreg': 'nickname' }),
    (r'^openid/complete/$', 'django_openidconsumer.views.complete'),
    (r'^openid/signout/$', 'django_openidconsumer.views.signout'),

    ('', include('myLibrary.web.urls')),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns('',
    ('^(?P<what>.*)$', 'views.bad')
)
