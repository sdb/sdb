from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
  (r'^stream/', include('sdb.social.urls')),
  (r'^admin/', include(admin.site.urls)),
  (r'^$', 'django.views.generic.simple.redirect_to', {'url': 'stream'}),
)

if settings.DEBUG:
  urlpatterns += patterns('django.views.static',
  (r'^media/(?P<path>.*)$', 
    'serve', {
    'document_root': settings.MEDIA_ROOT,
    'show_indexes': True }),)
