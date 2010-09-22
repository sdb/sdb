from django.conf.urls.defaults import *

from sdb.social.views import *

urlpatterns = patterns('',
  url(r'^update/?$', update, name='update'),
  url(r'^search/?$', search_with_param, name='search_with_param'),
  url(r'^search/(?P<q>[\w\+]+)$', search, name='search'),
  url(r'^search/(?P<q>[\w\+]+)/page/(?P<page>\d+)$', search, name='search'),
  url(r'^$', index, name='social'),
  url(r'^page/(?P<page>\d+)$', index, name='social'),
  url(r'^(?P<typ>\w+)$', index_by_typ, name='social_by_typ'),
  url(r'^(?P<typ>\w+)/page/(?P<page>\d+)$', index_by_typ, name='social_by_typ'),
  url(r'^service/(?P<service>\w+)$', index_by_service, name='social_by_service'),
  url(r'^service/(?P<service>\w+)/page/(?P<page>\d+)$', index_by_service, name='social_by_service'),
)
