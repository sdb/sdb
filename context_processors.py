from django.conf import settings

def main(request):
  return {'title':settings.APP_TITLE,
          'favicon':settings.FAVICON,
          'blog':settings.BLOG_URL if hasattr(settings, 'BLOG_URL') else None,}
