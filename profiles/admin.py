from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import SurmandlUser

class SurmandlUserCreationForm(forms.ModelForm):
    """A Form for creating new users.  Includes all the requiered fields, plus a repeated password """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = SurmandlUser
        fields = ("email, first_name, last_name, relation")

    def clean_password2(self):
        #Check that the two password entres match
        data = self.cleaned_data
        password1 = data.get("password1")
        password2 = data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError(msg)
        return password2

    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(SurmandlUserCreationForm, self).save(commit=False)
        data = self.cleaned_data
        user.set_password(data["password1"])
        if commit:
            user.save()
        return user

