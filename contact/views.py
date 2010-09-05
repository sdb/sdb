from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

import simplejson as json

from social.models import Service


def index(request):
  twitter = ''
  identica = ''
  mailto = settings.CONTACT_MAILTO if hasattr(settings, 'CONTACT_MAILTO') else None
  services = Service.objects.filter(name='twitter') | Service.objects.filter(name='identica')
  for service in services:  
    if service.name == 'twitter':
      twitter = 'http://twitter.com/%s' %json.loads(service.args)['user']
    if service.name == 'identica':
      identica = 'http://identi.ca/%s' %json.loads(service.args)['user']
  return render_to_response('contact/index.html', {'mailto':mailto, 'twitter':twitter, 'identica':identica}, context_instance=RequestContext(request))
  


