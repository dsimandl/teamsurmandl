from django.views.generic import ListView
from django.core.exceptions import ImproperlyConfigured

from .models import Image

class AlbumView(ListView):

    template_name = 'gallery/home.html'
    model = Image
    queryset = Image.objects.distinct('albums')


class SlideShowView(ListView):

    template_name = 'gallery/slideshow.html'
    model = Image


    def get_queryset(self):
        if self.queryset is None:
            queryset = self.model.objects.filter(albums__id=self.kwargs.get("album_id"))
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'model'"
                                   % self.__class__.__name__)
        return queryset