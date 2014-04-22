import zipfile
import imghdr

from django import forms


from .models import Image

class ImageAdminForm(forms.ModelForm):

    image_zip = forms.FileField(widget=forms.FileInput(), label='Zip file of pictures', required=False)

    class Meta:
        model = Image
        fields = ('title', 'image', 'image_zip', 'albums', 'user', 'tags')

    def clean(self):
        cleaned_data = super(ImageAdminForm, self).clean()
        if cleaned_data.get("image_zip") is None is cleaned_data.get("image"):
            raise forms.ValidationError(u"Either an image or an image zip file must be uploaded")
        return cleaned_data

    def clean_image_zip(self):
        image_zip = self.cleaned_data['image_zip']
        #If both are None the clean method above will catch it
        if image_zip is None:
            return image_zip
        elif not zipfile.is_zipfile(image_zip):
            raise forms.ValidationError(u"The file is not a zip file")
        else:
            return image_zip

    def clean_image(self):
        image = self.cleaned_data['image']
        if image is None:
            return image
        elif not imghdr.what(image):
            raise forms.ValidationError(u"The file is not an image file")
        else:
            return image

