from sdb.social.models import Link

def social(request):
  return {"social":{"links":Link.objects.order_by('title')}}
