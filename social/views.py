from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

import sys

import traceback

import simplejson as json

from datetime import datetime, timedelta

from social import feeder
from sdb.social.models import Entry, Service


def index(request):
  updates = []
  for entry in Entry.objects.order_by('-pub_date')[:100]:
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
    updater = feeder.updaters[service.name]
    # TODO: check null and log in case of null
    try:
      prev_update = service.updated
      if prev_update + timedelta(minutes=service.period) <= datetime.utcnow():
        updater(service)
        service.updated = datetime.utcnow()
        service.save()
    except:
      print traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
   
  return HttpResponseRedirect("/admin/")
