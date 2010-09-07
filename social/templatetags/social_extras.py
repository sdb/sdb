from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import re

import sdb.social.updater as updater


register = template.Library()

@register.filter(name='encode_status')
@stringfilter
def encode_status(value):
  return mark_safe(re.sub("(http://[^ ]*)", lambda m: '<a href="%s">%s</a>' % (m.group(1), m.group(1)), value))

@register.filter(name='profile')
def profile(value):
  if updater.registry.has_key(value.name):
    return updater.registry[value.name][1](value)
  return None

