from django.db import models

from imagekit.models import ProcessedImageField

from profiles.models import SurmandlUser

class Album(models.Model):
    title = models.CharField(max_length=60)
    public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

class Tag(models.Model):
    tag = models.CharField(max_length=50)

    def __unicode__(self):
        return self.tag

class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    image = ProcessedImageField(upload_to='gallery', format='JPEG', verbose_name='Image', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    albums = models.ManyToManyField(Album, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(SurmandlUser, null=True, blank=True)

    def __unicode__(self):
        return self.image.name


