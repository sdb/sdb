from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter(name='flickr_link')
def flickr_link(photo):
  return 'http://www.flickr.com/photos/%s/%s' %(photo.data['owner'], photo.photo_id)

@register.filter(name='flickr_photo')
def flickr_photo(photo):
  return 'http://farm%s.static.flickr.com/%s/%s_%s.jpg' %(photo.data['farm'], photo.data['server'], photo.photo_id, photo.data['secret'])
