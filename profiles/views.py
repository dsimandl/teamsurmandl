from django.views.generic.edit import UpdateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.http import Http404

from .forms import UserProfileForm
from .models import SurmandlUser

class SurmandlUserView(UpdateView):

    template_name = "profiles/profile.html"
    form_class = UserProfileForm
    success_url = '/home/'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SurmandlUserView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):

        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                return SurmandlUser.objects.filter(pk=self.request.user.pk)

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                      {'verbose_name': queryset.model._meta.verbose_name})
        return obj