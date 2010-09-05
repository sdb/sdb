from django.conf.urls.defaults import *

from sdb.about.views import index

urlpatterns = patterns('',
  url(r'^$', index, name='about'),
)
