from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


class CurrentLocation(TemplateView):

    template_name = 'location/current_location.html'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CurrentLocation, self).dispatch(request, *args, **kwargs)


class PastLocations(TemplateView):

    template_name = 'location/past_locations.html'
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PastLocations, self).dispatch(request, *args, **kwargs)
