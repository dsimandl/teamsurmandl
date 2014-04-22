from django.contrib import admin

from gallery.models import Album, Image
from .forms import ImageAdminForm

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title"]


class ImageAdmin(admin.ModelAdmin):

    form = ImageAdminForm

admin.site.register(Album, AlbumAdmin)
admin.site.register(Image, ImageAdmin)