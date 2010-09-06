from django.conf.urls.defaults import *

from sdb.social.views import index, update, search_with_param, search

urlpatterns = patterns('',
  url(r'^update$', update, name='update'),
  url(r'^search$', search_with_param, name='search_with_param'),
  url(r'^search/(?P<q>.+)$', search, name='search'),
  url(r'^$', index, name='social'),
  url(r'^(?P<typ>\w+)/$', index, name='social_by_typ'),
  url(r'^service/(?P<service>\w+)/$', index, name='social_by_service'),
)
