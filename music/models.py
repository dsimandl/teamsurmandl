from django.db import models

from profiles.models import SurmandlUser


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