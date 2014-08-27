import zipfile
import imghdr

from django import forms

from .models import Image, ImageBatchUpload, Album


class AlbumAdminForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = '__all__'

    def clean(self):

        cleaned_data = self.cleaned_data

        if cleaned_data.get('all_users') and cleaned_data.get('authorized_users').count() != 0:
            cleaned_data['all_users'] = False

        return cleaned_data

class ImageAdminForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('public', 'title', 'image', 'albums', 'user', 'tags')

    def clean_image(self):
        image = self.cleaned_data['image']
        if image is None:
            return image
        elif not imghdr.what(image):
            raise forms.ValidationError(u"The file is not an image file")
        else:
            return image

class ImageBatchUploadAdminForm(forms.ModelForm):

    class Meta:
        model = ImageBatchUpload
        fields = ('public', 'title', 'zip_file', 'albums', 'user', 'tags')

    def clean_zip_file(self):
        image_zip = self.cleaned_data['zip_file']
        if image_zip is None:
            return image_zip
        elif not zipfile.is_zipfile(image_zip):
            raise forms.ValidationError(u"The file is not a zip file")
        else:
            return image_zip
