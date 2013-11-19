from django.views.generic import UpdateView, ListView, FormView, DetailView
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.template.defaultfilters import slugify

from .models import Post
from .forms import PostCreateForm, PostViewForm

class PublishedPostMixin(object):

    def get_queryset(self):
        queryset = super(PublishedPostMixin, self).get_queryset()
        return queryset.filter(published=True)

class PostListView(PublishedPostMixin, ListView):

    model = Post

class PostDetailView(PublishedPostMixin, DetailView, FormMixin):

    model = Post
    form_class = PostViewForm
    template_name = 'blog/post_detail.html'
    success_url = '/blog/'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostDetailView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

class PostCreateView(FormView):

    form_class = PostCreateForm
    template_name = 'blog/post_create_update.html'
    success_url = '/blog/'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.fields['slug'] = slugify(form.fields['title'])
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

class PostEditView(PublishedPostMixin, UpdateView):

    model = Post
    template_name = 'blog/post_create_update.html'
    form_class = PostCreateForm
    success_url = "/blog/"

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostEditView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

