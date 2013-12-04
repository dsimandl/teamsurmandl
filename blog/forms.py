from django import forms

from .models import Post, PostComment

class PostCreateForm(forms.ModelForm):

    class Meta:

        model = Post
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),
            'photo': forms.FileInput(),
        }
