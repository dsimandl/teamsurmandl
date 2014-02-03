from django import forms

from .models import Post

class PostCreateForm(forms.ModelForm):

    clearPhoto = forms.BooleanField(required=False, label="Clear Photo")

    class Meta:

        model = Post
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),
            'photo': forms.FileInput(attrs={'title': 'Test'}),
        }


class PostReadForm(forms.ModelForm):

    class Meta:

        model = Post
        exclude = ['title', 'published']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),
        }


class PostFinalForm(forms.ModelForm):

    class Meta:

        model = Post





