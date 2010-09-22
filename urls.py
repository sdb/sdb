from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from sdb.sitemap import MainSitemap

admin.autodiscover()

sitemaps = {
    'flatpages': FlatPageSitemap,
    'main' : MainSitemap,
}

urlpatterns = patterns('',
  (r'^home/', include('sdb.home.urls')),
  (r'^contact/', include('sdb.contact.urls')),
  (r'^stream/', include('sdb.social.urls')),
  (r'^admin/', include(admin.site.urls)),
  (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

if settings.DEBUG:
  urlpatterns += patterns('django.views.static',
  (r'^media/(?P<path>.*)$', 
    'serve', {
    'document_root': settings.MEDIA_ROOT,
    'show_indexes': True }),)

urlpatterns += patterns('',
  (r'^', include('sdb.core.urls')),)
  
