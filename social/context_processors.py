from sdb.social.models import Link, Service

from datetime import datetime

from django.db.models import Max
from django.conf import settings

def social(request):
  # TODO handle case: no services found in database
  last_update = Service.objects.aggregate(Max('updated'))['updated__max']
  elapsed = (datetime.utcnow() - last_update).seconds / 60 if last_update != None else 1000
  return {'title':settings.APP_TITLE,
          'last_update':last_update,
          'elapsed':elapsed,
          'social':{'links':Link.objects.order_by('title')}}
