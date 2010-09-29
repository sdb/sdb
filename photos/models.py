from django.db import models
from sdb import models as sdb_models


class Photo(models.Model):
  photo_id = models.BigIntegerField()
  title         = models.TextField()
  description   = models.TextField(blank=True)
  date_taken    = models.DateTimeField()
  data = sdb_models.DictionaryField(max_length=2000)

  def __str__(self):
    return self.title

  class Meta:
    ordering = ['date_taken']
