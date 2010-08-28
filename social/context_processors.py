from sdb.social.models import Link

from django.conf import settings

def social(request):
  return {"title":settings.APP_TITLE, "social":{"links":Link.objects.order_by('title')}}
