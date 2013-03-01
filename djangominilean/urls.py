from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib import auth

admin.autodiscover()

urlpatterns = patterns('djangominilean.views',
    url(r'^$', 'home'),
    (r'^reset/?$', 'reset'),
    (r'^loadexperiment/?$', 'loadexperiment'),
    (r'^fbshare/(?P<code>[^/]+)/?$', 'fbshare'),

    url(r'^admin/', include(admin.site.urls)),
)
