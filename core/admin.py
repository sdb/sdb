from django.contrib import admin
from sdb.core.models import Content

class ContentAdmin(admin.ModelAdmin):
  list_display = ['key']

admin.site.register(Content, ContentAdmin)
