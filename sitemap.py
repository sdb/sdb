from django.contrib.sitemaps import Sitemap
from django.db.models import Max
from sdb.social.models import Entry
from django.core.urlresolvers import reverse
from datetime import datetime

class MainSitemap(Sitemap):

  def items(self):
    return ['home', 'contact', 'social', 'photos.index']

  def location(self, obj):
    return reverse(obj)
