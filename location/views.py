from django.views.generic import TemplateView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .models import Location

class CurrentLocation(DetailView):

    template_name = 'location/current_location.html'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CurrentLocation, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            obj = Location.objects.get(current_location=True)
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                      {'verbose_name': queryset.model._meta.verbose_name})
        return obj

class PastLocations(TemplateView):

    template_name = 'location/past_locations.html'
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PastLocations, self).dispatch(request, *args, **kwargs)
