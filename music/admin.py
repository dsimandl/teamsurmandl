import oauth2 as oauth
import urllib
import json

from django.contrib import admin

from .models import Music
from .rdio_api_config import CONSUMER_KEY, CONSUMER_SECRET, DEFAULT_ALBUM_IMAGE_URL

class MusicAdmin(admin.ModelAdmin):

    fields = ('song_title', 'album_name', 'artist_name', 'comments', 'added_by')

    def save_model(self, request, obj, form, change):
        consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        client = oauth.Client(consumer)
        response, content = client.request('http://api.rdio.com/1/', 'POST', urllib.urlencode({'method': 'search',
                                                                'query': '%s %s' % (obj.album_name, obj.artist_name),
                                                                'types': 'Album',
                                                                'count': 1}))
        parsed_content = json.loads(content)
        status = parsed_content['status']
        if status == 'error':
            obj.album_image_url = DEFAULT_ALBUM_IMAGE_URL
        else:
            obj.album_image_url = getpicurl(parsed_content['result'])
        obj.save()

def getpicurl(resultsdic):
    if resultsdic['album_count'] == 0:
        return DEFAULT_ALBUM_IMAGE_URL
    else:
        return resultsdic['results'][0].get('icon')



admin.site.register(Music, MusicAdmin)