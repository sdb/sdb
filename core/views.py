from django.shortcuts import render_to_response
from django.template import RequestContext
from sdb.core.models import Content


def wiki(request, page):
  try:
    content = Content.objects.get(key='wiki.%s' %page)
  except Content.DoesNotExist:
    content = None
  # TODO use regular 404 handling
  return render_to_response('wiki.html',
                            {"page_content":content.text if content != None else "Oops! Not found!"},
                            context_instance=RequestContext(request))
  


