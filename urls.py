from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
  (r'^home/', include('sdb.home.urls')),
  (r'^contact/', include('sdb.contact.urls')),
  (r'^about/', include('sdb.about.urls')),
  (r'^stream/', include('sdb.social.urls')),
  (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
  urlpatterns += patterns('django.views.static',
  (r'^media/(?P<path>.*)$', 
    'serve', {
    'document_root': settings.MEDIA_ROOT,
    'show_indexes': True }),)

urlpatterns += patterns('',
  (r'^', include('sdb.core.urls')),)
  
