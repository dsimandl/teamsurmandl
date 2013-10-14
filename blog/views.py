from django.views.generic import DetailView, UpdateView, ListView, FormView

from .models import Post
from .forms import PostCreateForm

class PublishedPostMixin(object):

    def get_queryset(self):
        queryset = super(PublishedPostMixin, self).get_queryset()
        return queryset.filter(published=True)

class PostListView(PublishedPostMixin, ListView):

    model = Post

class PostDetailView(PublishedPostMixin, DetailView):

    model = Post

class PostCreateView(FormView):

    form_class = PostCreateForm
    template_name = 'blog/post_create.html'

class PostEditView(PublishedPostMixin, UpdateView):

    model = Post