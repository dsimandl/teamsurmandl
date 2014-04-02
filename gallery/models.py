from django.db import models

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager

from profiles.models import SurmandlUser

class Album(models.Model):
    title = models.CharField(max_length=60)
    public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    image = ProcessedImageField(upload_to='gallery', format='JPEG', verbose_name='Image', blank=True)
    image_thumb = ImageSpecField(source='image', processors=[ResizeToFill(80,80)], format='JPEG', options={'quality': 60})
    albums = models.ManyToManyField(Album, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(SurmandlUser, null=True, blank=True)

    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.image.name


