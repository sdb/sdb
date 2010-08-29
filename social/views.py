from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from jogging import logging

import sys, traceback
import simplejson as json

from datetime import datetime, timedelta

from social import feeder
from social.models import Entry, Service


def index(request, typ=""):
  updates = []
  entries = Entry.objects.order_by('-pub_date')[:50] if typ == '' else Entry.objects.filter(typ=typ).order_by('-pub_date')[:50]
  for entry in entries:
    update = {'pub_date':entry.pub_date}
    update['entry'] = entry
    if entry.typ == 'photos':
      update['data'] = json.loads(entry.data)[:6]
    else:
      update['data'] = json.loads(entry.data)
    updates.append(update)
  return render_to_response('social/index.html', {'updates':updates}, context_instance=RequestContext(request))
  

def update(request):
  services = Service.objects.all()
  for service in services:
    if feeder.updaters.has_key(service.name):
      updater = feeder.updaters[service.name]
      try:
        prev_update = service.updated
        if prev_update + timedelta(minutes=service.period) <= datetime.utcnow():
          updater(service)
          service.updated = datetime.utcnow()
          service.save()
      except:
        logging.exception('updater exception for service %s' %service.name)
    else:
      logging.warning('updater for service %s not found' %service.name)
   
  return HttpResponseRedirect(request.GET.get('redirect') if 'redirect' in request.GET else reverse('social'))
