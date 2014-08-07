import os
import zipfile
import time
from io import BytesIO

from django.db import models
from django.core.files.base import ContentFile
from django.utils.image import Image as D_Image

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager

from profiles.models import SurmandlUser


class Album(models.Model):
    title = models.CharField(max_length=60)
    public = models.BooleanField(default=False)
    all_users = models.BooleanField(default=True)
    authorized_users = models.ForeignKey(SurmandlUser, null=True, blank=True)

    def __unicode__(self):
        return self.title


class ImageBatchUpload(models.Model):
    title = models.CharField(max_length=60, blank=True, help_text="If supplied here, images uploaded will be given this "
                                                      "title plus a sequential number. "
                                                      "If no title is supplied, the title will be the image filename")
    zip_file = models.FileField(upload_to='gallery/temp', help_text="Select a .zip file to upload into the album")
    albums = models.ForeignKey(Album, help_text="Select an album to add the images too.")
    user = models.ForeignKey(SurmandlUser, null=True)
    public = models.BooleanField(default=False, help_text="Click here to make these images public")

    tags = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        super(ImageBatchUpload, self).save(*args, **kwargs)
        self.process_zipfile()
        super(ImageBatchUpload, self).delete()

    def process_zipfile(self):
        if os.path.isfile(self.zip_file.path):
            zip = zipfile.ZipFile(self.zip_file.path)
            bad_file = zip.testzip()
            if bad_file:
                zip.close()
                raise Exception('"%s" in zip archive is corrupt' % bad_file)
            count = 1
            for file_name in sorted(zip.namelist()):
                if os.path.dirname(file_name):
                    continue
                if file_name.startswith('__') or file_name.startswith('.'):
                    continue
                data = zip.read(file_name)
                if not len(data):
                    continue
                try:
                    file = BytesIO(data)
                    opened = D_Image.open(file)
                    opened.verify()
                except Exception:
                    raise Exception('"%s" is a bad image file' % format(data))
                if not self.title:
                    title = '_'.join([format(file_name), str(count)])
                else:
                    title = '_'.join([self.title, str(count)])
                image = Image(title=title,
                              created=time.time(),
                              public=self.public,
                              user=self.user,)
                content_file = ContentFile(data)
                image.image.save(file_name, content_file)
                image.save()
                image.albums.add(self.albums)
                image.save()
                count += 1
            zip.close()
            return ""

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


