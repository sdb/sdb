from django.db import models

class Content(models.Model):
  key = models.CharField(max_length=100)
  text = models.TextField()
