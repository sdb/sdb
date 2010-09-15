from django.views.generic.list_detail import object_list
from social.models import Entry, Service


def index(request):
  entries = Entry.objects.all().order_by('-pub_date')[:5]
  return object_list(request,
    template_name='home/index.html',
    queryset=entries
  )
