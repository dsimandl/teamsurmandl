from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field, Submit
from crispy_forms.bootstrap import FormActions

from .models import Post

class PostCreateForm(forms.ModelForm):

    class Meta:

        model = Post
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'})
        }
