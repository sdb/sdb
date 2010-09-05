from sdb.social.models import Service, Entry, Link
from django.contrib import admin
from datetime import datetime

def reset_service(modeladmin, request, queryset):
  queryset.update(updated=datetime.min)
  for s in queryset:
    Entry.objects.filter(service=s).delete()
reset_service.short_description = 'Reset selected services'

class ServiceAdmin(admin.ModelAdmin):
  list_display = ['title', 'name', 'desc', 'period', 'updated', 'args', 'props']
  actions = [reset_service]

class EntryAdmin(admin.ModelAdmin):
  list_display = ['desc', 'typ', 'service', 'pub_date', 'data']
  list_filter = ['typ', 'desc']
  search_fields = ['data']

class LinkAdmin(admin.ModelAdmin):
  list_display = ['title', 'url']

admin.site.register(Service, ServiceAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Link, LinkAdmin)
