from django.views.generic import ListView
from django.core.exceptions import ImproperlyConfigured
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .models import Image, Album


class AlbumView(ListView):

    template_name = 'gallery/home.html'
    model = Image
    queryset = Image.objects.distinct('albums')

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumView, self).dispatch(request, *args, **kwargs)

class AlbumListView(ListView):

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumListView, self).dispatch(request, *args, **kwargs)

    template_name = 'gallery/single_home.html'
    model = Image

    def get_queryset(self):
        if self.queryset is None:
            queryset = self.model.objects.filter(albums__id=self.kwargs.get("album_id"))
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'model'"
                                   % self.__class__.__name__)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AlbumListView, self).get_context_data(**kwargs)
        context.update({'album_id': self.kwargs.get("album_id")})
        return context

class SlideShowView(ListView):

    template_name = 'gallery/slideshow.html'
    model = Image

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SlideShowView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.queryset is None:
            image_selected = self.model.objects.get(id=self.kwargs.get("image_id"))
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'model'"
                                   % self.__class__.__name__)
        return image_selected

    def get_context_data(self, **kwargs):
        context = super(SlideShowView, self).get_context_data(**kwargs)
        image_album = Album.objects.get(id=self.kwargs.get("album_id"))
        context.update({'album_images': image_album.image_set.all()})
        return context
