from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings

import simplejson as json

from social.models import Entry


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
  import updater
  updater.update()
  return HttpResponseRedirect(request.GET.get('redirect') if 'redirect' in request.GET else reverse('social'))
