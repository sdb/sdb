from sdb.social.models import Service, Entry, Link
from django.contrib import admin
from datetime import datetime
import updater

def reset_services(modeladmin, request, queryset):
  queryset.update(updated=datetime.min)
  for s in queryset:
    Entry.objects.filter(service=s).delete()
reset_services.short_description = 'Reset selected services'

def update_services(modeladmin, request, queryset):
  updater.update(queryset)
update_services.short_description = 'Update selected services'

def show_hide_profile(modeladmin, request, queryset):
  for s in queryset:
    s.show_profile = not s.show_profile
    s.save()
show_hide_profile.short_description = 'Show/hide profile for selected services'

def include_update(modeladmin, request, queryset):
  for s in queryset:
    s.include_update = not s.include_update
    s.save()
include_update.short_description = 'Include/exclude updates for selected services'

class ServiceAdmin(admin.ModelAdmin):
  list_display = ['title', 'name', 'desc', 'period', 'show_profile', 'include_update','ranking', 'updated', 'args', 'props']
  actions = [reset_services, update_services, show_hide_profile, include_update]

class EntryAdmin(admin.ModelAdmin):
  list_display = ['uuid', 'desc', 'typ', 'service', 'pub_date', 'data']
  list_filter = ['typ', 'desc']
  search_fields = ['data']

class LinkAdmin(admin.ModelAdmin):
  list_display = ['title', 'url']

admin.site.register(Service, ServiceAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Link, LinkAdmin)
