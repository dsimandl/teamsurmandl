from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import SurmandlUser

class SurmandlUserCreationForm(forms.ModelForm):
    """A Form for creating new users.  Includes all the required fields, plus a repeated password """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = SurmandlUser
        fields = ("email", "first_name", "last_name", "relation",)

    def clean_password2(self):
        #Check that the two password entries match
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

class SurmandlUserChangeForm(forms.ModelForm):
    """A form for updating users.  Includes all fields on the user, but replaces the password field with the admin's password hash display field """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = SurmandlUser

    def clean_password(self):
        """ Regardless of what the user provides, return the initial value.  This is doe here, rather than on the field, because the field does not have access to the initial value """
        return self.initial["password"]


class SurmandlUserAdmin(UserAdmin):
    #Set the add/modify forms
    add_form = SurmandlUserCreationForm
    form = SurmandlUserChangeForm

    # The fields to be used in displaying the User Model.
    # These override the definitions on the base UserAdmin that reference the specific fields on the auth.User
    list_display = ("email", "is_staff", "first_name", "last_name", "relation")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "relation")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)
        }),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",),
               "fields": ("email", "first_name", "last_name", "relation", "password1", "password2")}
        ),
    )

admin.site.register(
    SurmandlUser,
    SurmandlUserAdmin
)

