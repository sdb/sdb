from django.conf.urls.defaults import *

from sdb.core.views import wiki

urlpatterns = patterns('',
  url(r'^$', 'django.views.generic.simple.redirect_to', {'url': 'home'}, name='index'),
)
