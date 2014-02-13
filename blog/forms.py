from django import forms

from .models import Post

class PostCreateForm(forms.ModelForm):
    """
    Post Creation form with customized inputs and a clear photo checkbox
    """

    clearPhoto = forms.BooleanField(required=False, label="Clear Photo")

    class Meta:

        model = Post
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),
            'photo': forms.FileInput(attrs={'title': 'Test'}),
        }


class PostReadForm(forms.ModelForm):
    """
    Form to read a post with some customization for the content section
    """

    class Meta:

        model = Post
        exclude = ['title', 'published']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),
        }


class PostFinalForm(forms.ModelForm):

    """
    Simple form for the post preview
    """

    class Meta:

        model = Post





