from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.http import urlquote_plus
from django.db.models import Q
from django.contrib import messages

import simplejson as json

from social.models import Entry, Service


def index(request, typ="", service=""):
  updates = []
  per_page = settings.ENTRIES_PER_PAGE
  entries = Entry.objects
  if typ != '':
    entries = entries.filter(typ=typ)
  if service != '':
    s = Service.objects.filter(name=service)
    if len(s) > 0:
      entries = entries.filter(service=s[0])
  entries = entries.order_by('-pub_date')[:per_page]
  updates = prepare_entries(entries)
  return render_to_response('social/index.html', {'updates':updates}, context_instance=RequestContext(request))


def update(request):
  import updater
  msg = updater.update()
  messages.add_message(request, messages.INFO, msg)
  return HttpResponseRedirect(request.GET.get('redirect') if 'redirect' in request.GET else reverse('social'))


def search_with_param(request):
  return HttpResponseRedirect(reverse('search', args=[urlquote_plus(request.GET.get('search'))]))


def search(request, q):
  per_page = settings.ENTRIES_PER_PAGE
  terms = q.split("+")
  queries = [Q(data__contains=term) for term in terms]
  query = queries.pop()
  for item in queries:
    query &= item
  entries = Entry.objects.filter(query).order_by('-pub_date')[:per_page]
  updates = prepare_entries(entries)
  q = q.replace('+', ' ')
  messages.add_message(request, messages.INFO, '%d search result(s) for "%s"' %(len(updates), q))
  return render_to_response('social/index.html', {'updates':updates, 'query':q}, context_instance=RequestContext(request))


def prepare_entries(entries):
  updates = []
  for entry in entries:
    update = {'pub_date':entry.pub_date}
    update['entry'] = entry
    if entry.typ == 'photos':
      update['data'] = json.loads(entry.data)[:6]
    else:
      update['data'] = json.loads(entry.data)
    updates.append(update)
  return updates
  


