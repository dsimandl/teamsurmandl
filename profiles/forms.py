from django import forms

from .models import SurmandlUser

class UserProfileForm(forms.ModelForm):

    class Meta:

        model = SurmandlUser
        fields = {'email', 'first_name', 'last_name', 'relation'}

        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control", "id": "first_name", "placeholder": "First Name"}),
            'last_name': forms.TextInput(attrs={"class": "form-control", "id": "last_name", "placeholder": "Last Name"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "id": "email", "placeholder": "Email"}),
            'relation': forms.HiddenInput(),
        }

