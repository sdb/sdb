from django.shortcuts import render_to_response
from django.template import RequestContext
from social.models import Entry, Service
from photos.models import Photo


def index(request):
  entries = Entry.objects.all().order_by('-pub_date')[:5]
  photos = Photo.objects.all().order_by('?')[:6]
  return render_to_response('home/index.html', {'object_list':entries, "photos":photos}, context_instance=RequestContext(request))
