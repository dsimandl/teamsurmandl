from django import forms

from .models import Post

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





