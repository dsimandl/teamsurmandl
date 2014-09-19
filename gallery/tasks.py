import time
import zipfile
from io import BytesIO

from django.utils.image import Image as D_Image
from django.core.files.base import ContentFile

from celery import task

from .models import Image

@task
def upload_zip(to_upload):
    print("In the zip!")
    zip = zipfile.ZipFile(to_upload.zip_file)
    bad_file = zip.testzip()
    if bad_file:
        zip.close()
        raise Exception('"%s" in zip archive is corrupt' % bad_file)
    count = 1
    for file_name in sorted(zip.namelist()):
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
            raise Exception('"%s" is a bad image file' % format(file_name))
        if not to_upload.title:
            title = '_'.join([format(file_name), str(count)])
        else:
            title = '_'.join([to_upload.title, str(count)])
        image = Image(title=title,
                      created=time.time(),
                      public=to_upload.public,
                      user=to_upload.user, )
        content_file = ContentFile(data)
        image.image.save(file_name, content_file)
        image.save()
        image.albums.add(to_upload.albums)
        image.save()
        count += 1
    zip.close()
    return "Zip file uploaded!!"