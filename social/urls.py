from django.conf.urls.defaults import *

from sdb.social.views import index, update

urlpatterns = patterns('',
  url(r'^update$', update, name='update'),
  url(r'^$', index, name='social'),
)
