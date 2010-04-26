# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import direct_to_template, redirect_to
from yawp.feeds import RssArticleFeed, AtomArticleFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

feeds = {
    'rss': RssArticleFeed,
    'atom': AtomArticleFeed,
}

path_re = '(?P<path>([\.\w/-]+))'

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': '/blog/'}, name='index'),
    url(r'^cv/$', direct_to_template, {'template': 'static/cv.html' }, name='cv'),
    (r'^blog/', include('yawp.blog.urls')),
    url(r'^contact/', 'yawp.contact.views.index', name='contact'),
    url(r'^projects/', direct_to_template, {'template': 'static/projects.html'}, name='projects'),
    url(r'^search/$', 'yawp.search.views.search', name='search'),
    url(r'^explorer/$', 'yawp.explorer.views.list'),
    url(r'^explorer/dir@%(path_re)s$' % locals(), 'yawp.explorer.views.list'),
    url(r'^explorer/file@%(path_re)s$' % locals(), 'yawp.explorer.views.detail'),

    # Atom / RSS
    (r'^feeds/(?P<url>(rss|atom).*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^comments/', include('django.contrib.comments.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
