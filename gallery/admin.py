from django.contrib import admin

from gallery.models import Album, Image, ImageBatchUpload
from .forms import ImageAdminForm, ImageBatchUploadAdminForm

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title"]


class ImageAdmin(admin.ModelAdmin):

    form = ImageAdminForm


class BatchImageAdmin(admin.ModelAdmin):

    form = ImageBatchUploadAdminForm

admin.site.register(Album, AlbumAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ImageBatchUpload, BatchImageAdmin)
