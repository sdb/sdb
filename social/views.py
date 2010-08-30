from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings

from jogging import logging

import sys, traceback, threading
import simplejson as json

from datetime import datetime, timedelta

from social import feeder
from social.models import Entry, Service


def index(request, typ=""):
  updates = []
  per_page = settings.ENTRIES_PER_PAGE
  entries = Entry.objects.order_by('-pub_date')[:per_page] if typ == '' else Entry.objects.filter(typ=typ).order_by('-pub_date')[:per_page]
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
  if (settings.UPDATE_THREAD):
    UpdateThread().start()
  else:
    do_update()
  return HttpResponseRedirect(request.GET.get('redirect') if 'redirect' in request.GET else reverse('social'))
  

def do_update():
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
   

class UpdateThread ( threading.Thread ):
  def run ( self ):
    do_update()
