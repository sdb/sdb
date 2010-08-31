from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages

from jogging import logging

import sys, traceback, threading
import simplejson as json

from datetime import datetime, timedelta

from social import feeder
from social.models import Entry, Service


running_update = False
running_update_lock = threading.RLock()


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
  global running_update
  global running_update_lock
  to_update = []
  services = Service.objects.all()
  for service in services:
    if feeder.updaters.has_key(service.name):
      prev_update = service.updated
      if prev_update + timedelta(minutes=service.period) <= datetime.utcnow():
        to_update.append(service)  
    else:
      logging.warning('updater for service %s not found' %service.name)
  running_update_lock.acquire()
  if not running_update and len(to_update) > 0:
    running_update = True
    if (settings.UPDATE_THREAD):
      UpdateThread(to_update).start()
    else:
      do_update(to_update)
    messages.add_message(request, messages.INFO, 'Thank you! %d services are scheduled for an update.' %len(to_update))
  else:
    messages.add_message(request, messages.INFO, 'Nothing to feed! All services are up-to-date. Thanks anyway!')
  running_update_lock.release()
  return HttpResponseRedirect(request.GET.get('redirect') if 'redirect' in request.GET else reverse('social'))
  

def do_update(services):
  global running_update
  global running_update_lock
  
  for service in services:
    updater = feeder.updaters[service.name]
    try:
      updater(service)
      service.updated = datetime.utcnow()
      service.save()
    except:
      logging.exception(msg='updater exception for service %s' %service.name, exception=True)
  running_update_lock.acquire()
  running_update = False
  running_update_lock.release()

class UpdateThread ( threading.Thread ):
  
  def __init__(self, services=None):
    threading.Thread.__init__(self)
    self.services = services

  def run ( self ):
    do_update(self.services)

