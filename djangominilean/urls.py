from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('djangominilean.views',
    url(r'^$', 'home', name='home_link'),
    (r'^reset/?$', 'reset'),
    (r'^fbshare/(?P<code>[^/]+)/?$', 'fbshare'),
# Examples:
    # url(r'^$', 'djangominilean.views.home', name='home'),
    # url(r'^djangominilean/', include('djangominilean.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
