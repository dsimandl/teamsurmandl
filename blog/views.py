from django.views.generic import DetailView, UpdateView, ListView

from blog.models import Post


class PublishedPostMixin(object):

    def get_queryset(self):
        queryset = super(PublishedPostMixin, self).get_queryset()
        return queryset.filter(published=True)

class PostListView(PublishedPostMixin, ListView):

    model = Post

class PostDetailView(PublishedPostMixin, DetailView):

    model = Post


class PostEditView(PublishedPostMixin, UpdateView):

    model = Post