from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter(name='flickr_link')
def flickr_link(photo):
  return 'http://www.flickr.com/photos/%s/%s' %(photo.data['owner'], photo.photo_id)
