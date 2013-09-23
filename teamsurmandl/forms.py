from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML, Div
from crispy_forms.bootstrap import FormActions

class SurmandlAuthForm(AuthenticationForm):

    username = forms.EmailField()
    password = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        #This removes all labels from the HTML
        self.helper.form_show_labels = False
        self.helper.form_show_errors = False
        self.helper.form_method = 'post'
        self.helper._form_action = ''
        self.helper.layout = Layout(
            HTML('<h2 class="form_signin-heading">Please sign in</h2>'),
            HTML('{% if form.non_field_errors %}<div class="login-alert alert-danger">{{ form.non_field_errors.as_text }}</div>{% endif %}' ),
            Field('username', css_class='form-control', placeholder="Email address", name="username", autofocus='True'),
            HTML('{% if form.username.errors %} <div class="login-alert alert-danger">{{ form.username.errors.as_text }}</div>{% endif %}'),
            Field('password', css_class='form-control', placeholder="Password", name="password"),
            HTML('{% if form.password.errors %} <div class="login-alert alert-danger">{{ form.password.errors.as_text }}</div>{% endif %}'),
            HTML('<label class="checkbox"> <input type="checkbox" value="remember-me"> Remember me</label>'),
            FormActions(
                Submit('submit', "Sign in", css_class="btn btn-large btn-primary btn-block")
            )
        )
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

