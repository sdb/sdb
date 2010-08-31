from sdb.social.models import Service, Entry, Link
from django.contrib import admin

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'period', 'updated', 'args', 'props']

class EntryAdmin(admin.ModelAdmin):
    list_display = ['desc', 'typ', 'pub_date', 'data']

class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']

admin.site.register(Service, ServiceAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Link, LinkAdmin)
