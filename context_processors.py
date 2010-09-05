from sdb.social.models import Link
from django.conf import settings

def main(request):
  return {'title':settings.APP_TITLE,
          'social':{'links':Link.objects.order_by('title')},
          'favicon':settings.FAVICON,
          'blog':settings.BLOG_URL if hasattr(settings, 'BLOG_URL') else None,}
