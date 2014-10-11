from django.views.generic.edit import UpdateView, FormView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect

from .forms import UserProfileForm, UserProfileChangePasswordForm
from .models import SurmandlUser


class SurmandlUserView(UpdateView):
    template_name = "profiles/profile.html"
    form_class = UserProfileForm
    success_url = '/'

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


class SurmandlUserPasswordChangeView(FormView):
    form_class = UserProfileChangePasswordForm
    template_name = 'profiles/password_change.html'
    success_message = 'Password changed successfull! '
    success_url = '/profile/password_change/'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SurmandlUserPasswordChangeView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs['user'] = self.request.user
        return form_class(**kwargs)

    def form_valid(self, form):
        form.save()
        # ToDo when upgrade to 1.7 update_session_auth_hash(self.request, form.user)
        messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())






