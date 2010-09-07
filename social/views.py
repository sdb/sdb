from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse, resolve
from django.conf import settings
from django.utils.http import urlquote_plus
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic.list_detail import object_list

import simplejson as json

from social.models import Entry, Service


def index(request, page=1):
  page = int(page)
  query = Q()
  entries = prepare_entries(query)
  return object_list(request,
    template_name='social/index.html',
    queryset=entries,
    paginate_by=settings.ENTRIES_PER_PAGE,
    page=page,
    context_processors=[lambda r: process_paging_context(r, 'social', page)]
  )


def index_by_typ(request, typ, page=1):
  page = int(page)
  query = Q(typ=typ)
  entries = prepare_entries(query)
  messages.add_message(request, messages.INFO, 'Found %d entries of type \'%s\'' %(len(entries), typ))
  return object_list(request,
    template_name='social/index.html',
    queryset=entries,
    paginate_by=settings.ENTRIES_PER_PAGE,
    page=page,
    context_processors=[lambda r: process_paging_context(r, 'social_by_typ', page, kwargs={'typ':typ})]
  )


def index_by_service(request, service, page=1):
  page = int(page)
  query = Q()
  service_obj = None
  if service != '':
    s = Service.objects.filter(name=service)
    if len(s) > 0:
      service_obj = s[0]
      query &= Q(service=service_obj)
  entries = prepare_entries(query)
  if service_obj != None:
    messages.add_message(request, messages.INFO, 'Found %d entries for service \'%s\'' %(len(entries), service_obj.title))
  return object_list(request,
    template_name='social/index.html',
    queryset=entries,
    paginate_by=settings.ENTRIES_PER_PAGE,
    page=page,
    context_processors=[lambda r: process_paging_context(r, 'social_by_service', page, kwargs={'service':service})]
  )


def update(request):
  import updater
  msg = updater.update()
  messages.add_message(request, messages.INFO, msg)
  return HttpResponseRedirect(request.GET.get('redirect') if 'redirect' in request.GET else reverse('social'))


def search_with_param(request):
  return HttpResponseRedirect(reverse('search', args=[urlquote_plus(request.GET.get('search'))]))


def search(request, q, page=1):
  page = int(page)
  terms = q.split("+")
  queries = [Q(data__contains=term) for term in terms]
  query = queries.pop()
  for item in queries:
    query &= item
  entries = prepare_entries(query)
  if q != '':
    messages.add_message(request, messages.INFO, '%d search result(s) for \'%s\'' %(len(entries), q.replace('+', ' ')))
  result =  object_list(request,
    template_name='social/index.html',
    queryset=entries,
    paginate_by=settings.ENTRIES_PER_PAGE,
    page=page,
    context_processors=[lambda r: process_paging_context(r, 'search', page, kwargs={'q':q})],
    extra_context={
      'query':q.replace('+', ' '),
    }
  )
  return result


def prepare_entries(query):
  if query != None:
    entries = Entry.objects.filter(query).order_by('-pub_date')
  else:
    entries = Entry.objects.all().order_by('-pub_date')
  return entries


def process_paging_context(request, view, page, kwargs={}):
  return {'next_page':reverse(view, kwargs=dict({'page':page+1},**kwargs)),
          'prev_page':reverse(view, kwargs=dict({'page':page-1},**kwargs))}
  


