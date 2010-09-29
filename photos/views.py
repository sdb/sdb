from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from sdb.photos.models import Photo


def sync(request):
  import sync
  try:
    sync.sync()  
  except:
    logging.exception(msg='error syncing flickr photos', exception=True)
  return HttpResponseRedirect(request.GET.get('redirect') if 'redirect' in request.GET else reverse('photos.index'))


def index(request):
  photos = Photo.objects.all()
  return render_to_response('photos/index.html', {'photos':photos}, context_instance=RequestContext(request))
  
