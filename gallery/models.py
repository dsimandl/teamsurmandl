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


class ImageBatchUpload(models.Model):
    title = models.CharField(max_length=60, help_text="If supplied here, images uploaded will be given this "
                                                      "title plus a sequential number. "
                                                      "If no title is supplied, the title will be the image filename")
    zip_file = models.FileField(upload_to='gallery/temp', help_text="Select a .zip file to upload into the album")
    albums = models.ManyToManyField(Album, null=True)
    user = models.ForeignKey(SurmandlUser, null=True)
    public = models.BooleanField(default=False, help_text="Click here to make these images public")

    tags = TaggableManager(blank=True)


class Image(models.Model):
    title = models.CharField(max_length=60, null=True)
    image = ProcessedImageField(upload_to='gallery', format='JPEG', verbose_name='Image', blank=True)
    image_thumb = ImageSpecField(source='image', processors=[ResizeToFill(140,140)], format='JPEG', options={'quality': 60})
    albums = models.ManyToManyField(Album, null=True)
    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    user = models.ForeignKey(SurmandlUser, null=True)

    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.image.name


