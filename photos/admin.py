from sdb.photos.models import Photo
from django.contrib import admin

class PhotoAdmin(admin.ModelAdmin):
  list_display = ['title', 'description', 'date_taken', 'data']

admin.site.register(Photo, PhotoAdmin)
