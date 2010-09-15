from django.shortcuts import render_to_response
from django.template import RequestContext
from sdb.core.models import Content


def index(request):
  try:
    content = Content.objects.get(key='about')
  except Content.DoesNotExist:
    content = None
  return render_to_response('about/index.html',
                            {"about":content.text if content != None else "Coming soon!"},
                            context_instance=RequestContext(request))
  


