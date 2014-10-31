import json

from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.utils.decorators import method_decorator
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from taggit.models import Tag
from pytz import timezone

from .models import Post, PostComment
from .forms import PostCommentForm

class PublishedPostMixin(object):
    """
    This sets the queryset to return only published posts
    """

    def get_queryset(self):
        queryset = super(PublishedPostMixin, self).get_queryset()
        return queryset.filter(published=True)

class TagMixin(object):
    """
    Mixin for all the posts we want tagged
    """

    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class AjaxableResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context, cls=DjangoJSONEncoder)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        if self.request.is_ajax():
            self.object = form.save()
            my_datetime = self.object.created_at.astimezone(timezone('US/Eastern')).strftime("%b. %d, %Y, %I:%M %p")
            delete_url = reverse('blog:delete', args=(self.object.id,))
            data = {'comment': self.object.comment, 'first_name': self.object.author.first_name, 'last_name': self.object.author.last_name, 'created_at': my_datetime, 'delete_url': delete_url, 'comment_id': self.object.id }
            return self.render_to_json_response(data)
        else:
            return response


class PostListView(PublishedPostMixin,TagMixin, ListView):
    """
    Simple view to list all of our blog posts
    """

    template_name = 'blog/post_list.html'
    model = Post
    paginate_by = 5

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostListView, self).dispatch(request, *args, **kwargs)

class PostTagIndexView(TagMixin, ListView):
    """
    View to list our blog posts by tags
    """

    template_name = 'blog/post_list.html'
    model = Post
    paginate_by = 5
    http_method_names = ['get', 'post']

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostTagIndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(post_tags__slug=self.kwargs.get('slug'), published=True)

class PostTitleIndexView(TagMixin, ListView, ):
    """
    View to list our blog posts by a title search
    """
    template_name = 'blog/post_list.html'
    model = Post
    paginate_by = 5


    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostTitleIndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        title_search = self.request.GET['title_search']
        if title_search == '':
            return Post.objects.all()
        else:
            return Post.objects.filter(title__icontains=title_search)


class PostDetailView(PublishedPostMixin, AjaxableResponseMixin, FormMixin, DetailView, ProcessFormView):
    """
    Edit view for our blog posts.  If the user is not an admin we direct them to the read form, otherwise they are directed to the edit form
    When the form is submitted we direct to the preview form
    """

    model = Post
    template_name = 'blog/post_create_update.html'
    form_class = PostCommentForm
    initial = {}
    success_url = '/blog/'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({'comments':(PostComment.objects.filter(post__pk=context['post'].pk))})

        self.initial = {'post': context['post'].pk, 'author': self.request.user.pk}
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context.update({'form': form})
        return context


def delete_comment(request, id):
        #Try/except here
        u = PostComment.objects.get(pk=id).delete()
        data = {'comment_id': id}
        return HttpResponse(json.dumps(data), content_type='application/json')


