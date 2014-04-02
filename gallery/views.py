from django.views.generic import ListView

from .models import Image

class AlbumView(ListView):

    template_name = 'gallery/home.html'
    model = Image
    queryset = Image.objects.order_by('created').distinct('album')


