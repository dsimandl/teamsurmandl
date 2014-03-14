from django.contrib import admin

from gallery.models import Album, Image

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title"]


class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["__unicode__", "title", "user", "created"]
    list_filter = ["albums"]

admin.site.register(Album, AlbumAdmin)
admin.site.register(Image, ImageAdmin)