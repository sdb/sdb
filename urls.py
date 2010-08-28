from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
  (r'^admin/', include(admin.site.urls)),
  (r'^update', 'social.views.update'),
  (r'^$', 'social.views.index'),
)

if settings.DEBUG:
  urlpatterns += patterns('django.views.static',
  (r'^media/(?P<path>.*)$', 
    'serve', {
    'document_root': settings.MEDIA_ROOT,
    'show_indexes': True }),)
