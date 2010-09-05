from django.conf.urls.defaults import *

from sdb.contact.views import index

urlpatterns = patterns('',
  url(r'^$', index, name='contact'),
)
