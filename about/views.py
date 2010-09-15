from django.shortcuts import render_to_response
from django.template import RequestContext
from sdb.core.models import Content


def index(request):
  try:
    content = Content.objects.get(key='about')
  except Content.DoesNotExist:
    content = "Coming soon!"
  return render_to_response('about/index.html', {"about":content.text}, context_instance=RequestContext(request))
  


