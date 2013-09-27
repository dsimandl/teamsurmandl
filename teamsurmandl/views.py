import urlparse
import logging
from django.views.generic import FormView, TemplateView
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import RedirectView
from django.conf import settings
from .forms import SurmandlAuthForm


logger = logging.getLogger(__name__)

class LoginView(FormView):
    form_class = SurmandlAuthForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "login.html"

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')
        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

class HomePageView(TemplateView):

    template_name = "home.html"

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HomePageView, self).dispatch(request, *args, **kwargs)


class LogOutView(RedirectView):

    url = settings.LOGIN_URL
    permanent = False

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(**kwargs)
        if self.request.user.is_authenticated:
            auth.logout(self.request)
        if url:
            if self.permanent:
                return HttpResponsePermanentRedirect(url)
            else:
                return HttpResponseRedirect(url)
        else:
            logger.warning('Gone: %s', self.request.path,
                    extra={
                        'status_code': 410,
                        'request': self.request
                    })
            return HttpResponseGone()