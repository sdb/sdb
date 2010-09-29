from django.conf.urls.defaults import *
from sdb.photos.views import sync, index

urlpatterns = patterns('',
  url(r'^$', index, name='photos.index'),
  url(r'^sync/?$', sync, name='photos.sync'),
)
