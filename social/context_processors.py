from sdb.social.models import Service, Link
from sdb.social import updater

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from datetime import datetime

from django.db.models import Max

def social(request):
  # TODO handle case: no services found in database
  last_update = Service.objects.aggregate(Max('updated'))['updated__max']
  elapsed = ((datetime.utcnow() - last_update).seconds / 60 if not updater.running_update else -1) if last_update != None else 1000
  if request.path.startswith(reverse('social')) and elapsed > settings.UPDATE_MSG_ELAPSED:
      messages.add_message(request, messages.INFO, 'It\'s been a while since the last update. Click <a href="%s">here</a> to schedule an update.' %reverse('update'))
  services = Service.objects.all()
  return {'last_update':last_update,
          'social':{'links':Link.objects.order_by('title')},
          'filter_services': services,
          'profile_services': filter(lambda s: s.show_profile, services),
          'elapsed':elapsed,}
