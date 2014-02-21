from django import forms

from .models import PostComment

class PostCommentForm(forms.ModelForm):
    """
    Form to read a post with some customization for the content section
    """

    class Meta:

        model = PostComment

        widgets = {
            'post': forms.HiddenInput(),
            'author': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),
        }





