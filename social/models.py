from django.db import models
from datetime import datetime

class Service(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=1023, blank=True)
    args = models.CharField(max_length=1023)
    period = models.IntegerField()
    updated = models.DateTimeField(blank=True, default=datetime.min)

class Entry(models.Model):
    desc = models.CharField(max_length=255)
    data = models.CharField(max_length=30000)
    pub_date = models.DateTimeField()
    typ = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Entries'
        ordering = ['-pub_date']

class Link(models.Model):
  title = models.CharField(max_length=255)
  url = models.URLField()
