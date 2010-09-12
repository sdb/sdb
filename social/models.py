from django.db import models
from datetime import datetime
import simplejson as json
from sdb import models as sdb_models


class Service(models.Model):
  name = models.CharField(max_length=255)
  title = models.CharField(max_length=255)
  desc = models.CharField(max_length=1023, blank=True)
  args = sdb_models.JSONField(max_length=1023)
  props = sdb_models.JSONField(max_length=1023)
  period = models.IntegerField()
  updated = models.DateTimeField(blank=True, default=datetime.min)
  show_profile = models.BooleanField(default=True)

  def __str__(self):
    return self.title

  class Meta:
    ordering = ['name']


class Entry(models.Model):
  desc = models.CharField(max_length=255)
  data = sdb_models.JSONField(max_length=30000)
  pub_date = models.DateTimeField()
  typ = models.CharField(max_length=255)
  service = models.ForeignKey('Service')
  uuid = models.CharField(max_length=255)

  def __str__(self):
    return self.desc

  class Meta:
    verbose_name_plural = 'Entries'
    ordering = ['-pub_date']


class Link(models.Model):
  title = models.CharField(max_length=255)
  url = models.URLField()

  def __str__(self):
    return self.title

  class Meta:
    ordering = ['title']
