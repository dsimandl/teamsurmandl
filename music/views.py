from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .models import Music

class MusicView(ListView):

    template_name = 'music/music.html'
    model = Music

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MusicView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(MusicView, self).get_queryset()
        return queryset.filter(added_by__first_name=self.kwargs.get("first_name"))
