from django.conf.urls.defaults import *

from sdb.home.views import *

urlpatterns = patterns('',
  url(r'^$', index, name='home'),
)
