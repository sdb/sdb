from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.safestring import SafeUnicode

import re

import sdb.social.updater as updater
from sdb.social.models import Service


register = template.Library()

@register.filter(name='encode_status')
@stringfilter
def encode_status(value):
  return mark_safe(re.sub("(http://[^ ]*)", lambda m: '<a href="%s">%s</a>' % (m.group(1), m.group(1)), value))

@register.filter(name='profile')
def profile(value):
  if isinstance(value, SafeUnicode):
    value = Service.objects.get(name=value)
  if updater.registry.has_key(value.name):
    return updater.registry[value.name][1](value)
  return None

