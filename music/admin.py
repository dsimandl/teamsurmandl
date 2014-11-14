from django.contrib import admin

from .models import Music


class MusicAdmin(admin.ModelAdmin):

    fields = ('song_title', 'album_name', 'artist_name', 'comments', 'added_by')


admin.site.register(Music, MusicAdmin)