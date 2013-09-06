from django.views.generic import FormView
from .forms import SurmandlAuthForm

class HomePageView(FormView):
    form_class = SurmandlAuthForm
    template_name = "login.html"