from django.views.generic import UpdateView, ListView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured

from .models import Post
from .forms import PostCreateForm

class PublishedPostMixin(object):

    def get_queryset(self):
        queryset = super(PublishedPostMixin, self).get_queryset()
        return queryset.filter(published=True)

class PostListView(PublishedPostMixin, ListView):

    model = Post

class PostDetailView(PublishedPostMixin, UpdateView):

    model = Post
    form_class = PostCreateForm
    template_name_update = 'blog/post_create_update.html'
    template_name_detail = 'blog/post_detail.html'
    success_url = '/blog/'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostDetailView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):

        if request.user.is_staff:
            self.object = self.get_object()
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            return self.render_to_response(self.get_context_data(object=self.object, form=form))
        else:
            self.object= self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def get_template_names(self):

        if self.request.user.is_staff:
            if self.template_name_update is None:
                raise ImproperlyConfigured("TemplateResponseMixin requires either a definition of "
                    "'template_name' or an implementation of 'get_template_names()'")
            else:
                return [self.template_name_update]
        else:
            if self.template_name_detail is None:
                raise ImproperlyConfigured("TemplateResponseMixin requires either a definition of "
                    "'template_name' or an implementation of 'get_template_names()'")
            else:
                return [self.template_name_detail]

class PostCreateView(FormView):

    form_class = PostCreateForm
    template_name = 'blog/post_create_update.html'
    success_url = '/blog/'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

class PostEditView(PublishedPostMixin, UpdateView):

    model = Post