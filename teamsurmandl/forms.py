from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class SurmandlAuthForm(AuthenticationForm):

    username = forms.EmailField()
    password = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.form_method = 'post'
        self.helper._form_action = ''
        self.helper.add_input(Submit('submit', "Submit"))
        super(SurmandlAuthForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
        if self.user_cache is None:
            raise forms.ValidationError("Your email and password do not match")
        elif not self.user_cache.is_active:
            raise forms.ValidationError("The account is inactive")

        return self.cleaned_data


