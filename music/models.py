import oauth2 as oauth
import urllib
import json


from django.db import models

from profiles.models import SurmandlUser
from .rdio_api_confg import CONSUMER_KEY, CONSUMER_SECRET, DEFAULT_ALBUM_IMAGE_URL


class Music(models.Model):
    song_title = models.CharField('Song Title', max_length=255)
    album_name = models.CharField('Album Name', max_length=255)
    artist_name = models.CharField('Artist Name', max_length=255)
    comments = models.TextField('Comments or thoughts on the music')
    added_by = models.ForeignKey(SurmandlUser, limit_choices_to={'is_staff': True},
                                 related_name='music', verbose_name='Music added by')
    album_image_url = models.TextField('URL for hosted album image')

    def __unicode__(self):
        return self.song_title

    def save(self, *args, **kwargs):
        consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        client = oauth.Client(consumer)
        # Hard coded for testing....
        response, content = client.request('http://api.rdio.com/1/', 'POST', urllib.urlencode({'method': 'search',
                                                                                      'query': 'Copper Blue Suger',
                                                                                      'types': 'Album',
                                                                                      'count': 1}))
        parsed_content = json.loads(content)
        status = parsed_content['status']
        if status == 'error':
            self.album_image_url = DEFAULT_ALBUM_IMAGE_URL
        else:
            self.album_image_url = getpicurl(parsed_content['result'])
        super(Music, self).save(*args, **kwargs)


def getpicurl(resultsdic):
    if resultsdic['album_count'] == 0:
        return DEFAULT_ALBUM_IMAGE_URL
    else:
        return resultsdic['results'][0].get('icon')