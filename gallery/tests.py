import os

from django.test import TestCase
from django.core.files import File
from model_mommy import mommy

from .models import Album, Image
from .forms import AlbumAdminForm, ImageAdminForm

here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

PROJECT_ROOT = here("..")
# root() gives us file paths from the root of the system to whatever
# folder(s) we pass it starting at the parent directory of the current file.
root = lambda *x: os.path.join(os.path.abspath(PROJECT_ROOT), *x)

class AlbumTest(TestCase):

    def setUp(self):

        self.new_album = mommy.make(Album, make_m2m=True)

    def test_album_create(self):

        self.assertTrue(isinstance(self.new_album, Album))
        self.assertEqual(self.new_album.__unicode__(), self.new_album.title)

    def test_valid_album_form(self):
        data = {'title': self.new_album.title, 'public': self.new_album.public, 'all_users': self.new_album.all_users,
                'authorized_users': ''}
        form = AlbumAdminForm(data=data)
        self.assertTrue(form.is_valid())

    def test_noneType_album_form(self):
        data = {'title': self.new_album.title, 'public': self.new_album.public, 'all_users': self.new_album.all_users,
                'authorized_users': None}
        form = AlbumAdminForm(data=data)
        self.assertTrue(form.is_valid())


class ImageTest(TestCase):

    def setUp(self):
        self.new_image = mommy.make(Image)

    def test_image_create(self):
        self.assertTrue(isinstance(self.new_image, Image))
        self.assertEqual(self.new_image.__unicode__(), self.new_image.title)

    def test_valid_image(self):
        with open(root('gallery/res/sample.jpg'), mode='rb') as f:
            test_file = File(f)
            test_image = mommy.make(Image, image=test_file)
            data = {'title': test_image.title, 'image': test_image.image, 'albums': test_image.albums, 'created': test_image.created,
                    'public': test_image.public, 'user': test_image.user}
            form = ImageAdminForm(data=data)
            self.assertTrue(form.is_valid)