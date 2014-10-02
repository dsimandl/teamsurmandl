from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, Transpose, SmartResize
from boto.s3.connection import S3Connection, Bucket, Key

from profiles.models import SurmandlUser


class Album(models.Model):
    title = models.CharField(max_length=60)
    public = models.BooleanField(default=False)
    all_users = models.BooleanField(default=True)
    authorized_users = models.ManyToManyField(SurmandlUser, null=True, blank=True)

    def __unicode__(self):
        return self.title


class ImageBatchUpload(models.Model):
    title = models.CharField(max_length=60, blank=True,
                             help_text="If supplied here, images uploaded will be given this "
                                       "title plus a sequential number. "
                                       "If no title is supplied, the title will be the image filename")
    zip_file = models.FileField(upload_to='gallery/temp', help_text="Select a .zip file to upload into the album")
    albums = models.ForeignKey(Album, help_text="Select an album to add the images too.")
    user = models.ForeignKey(SurmandlUser, null=True)
    public = models.BooleanField(default=False, help_text="Click here to make these images public")

    def save(self, *args, **kwargs):
        super(ImageBatchUpload, self).save(*args, **kwargs)
        from .tasks import upload_zip
        upload_zip.delay(self)
        super(ImageBatchUpload, self).delete()

class Image(models.Model):
    title = models.CharField(max_length=60, null=True)
    image = ProcessedImageField(upload_to='gallery', processors=[Transpose(), SmartResize(555, 417)], format='JPEG', verbose_name='Image')
    image_thumb = ImageSpecField(source='image', processors=[ResizeToFill(140, 140)], format='JPEG',
                                 options={'quality': 60})
    albums = models.ManyToManyField(Album, null=True)
    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    user = models.ForeignKey(SurmandlUser, null=True)

    def __unicode__(self):
        return self.title


@receiver(pre_delete, sender=Image)
def delete_img_aws(instance, **kwargs):
    conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    b = Bucket(conn, settings.AWS_STORAGE_BUCKET_NAME)
    img_k = Key(b)
    img_thumb_k = Key(b)
    img_k.key = instance.image.name
    img_thumb_k.key = instance.image_thumb.name
    b.delete_key(img_k)
    b.delete_key(img_thumb_k)