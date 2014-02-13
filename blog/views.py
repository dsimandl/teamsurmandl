

from django.views.generic import UpdateView, ListView, FormView, DetailView, CreateView
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.core.exceptions import ImproperlyConfigured
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

from taggit.models import Tag

from .models import Post, PostComment
from .forms import PostCreateForm, PostReadForm, PostFinalForm

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

class PostListView(PublishedPostMixin,TagMixin, ListView):
    """
    Simple view to list all of our blog posts
    """

    template_name = 'blog/post_list.html'
    model = Post
    paginate_by = 5

class PostTagIndexView(TagMixin, ListView):
    """
    View to list our blog posts by tags
    """

    template_name = 'blog/post_list.html'
    model = Post
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('slug'), published=True)

class PostEditView(PublishedPostMixin, UpdateView):
    """
    Edit view for our blog posts.  If the user is not an admin we direct them to the read form, otherwise they are directed to the edit form
    When the form is submitted we direct to the preview form
    """

    model = Post
    template_name = 'blog/post_create_update.html'
    form_class = PostCreateForm
    preview_url = '/blog/preview/'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostEditView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostEditView, self).get_context_data(**kwargs)
        if self.request.user.is_staff == False:
            context['comments'] = PostComment.objects.filter(post__pk=context['post'].pk)
        return context

    def get_form_class(self):
        if self.request.user.is_staff == False:
            return PostReadForm
        else:
            return PostCreateForm

    def get_success_url(self):
        if self.preview_url:
            url = force_text(self.preview_url)
        else:
            raise ImproperlyConfigured(
            "No URL to redirect to. Provide a success_url.")
        return url

    def form_valid(self, form):
        if not form['slug']:
            form['slug'] = slugify(form['title'])
        self.request.session['form'] = form
        return HttpResponseRedirect(self.get_success_url())


class PostCreateView(FormView):
    """
    View for our post create.  We store the form into the session if its valid
    """

    form_class = PostCreateForm
    template_name = 'blog/post_create_update.html'
    preview_url = '/blog/preview/'


    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.session['form'] = form
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.preview_url:
            url = force_text(self.preview_url)
        else:
            raise ImproperlyConfigured(
            "No URL to redirect to. Provide a success_url.")
        return url

#Think about how we can do this with cookies or html localstorage

class PostPreviewView(DetailView):
    """
    View for our preview form.
    """

    template_name = 'blog/post_preview.html'

    def get_object(self, queryset=None):
        obj = self.request.session._session['form']
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class HiddenFormView(CreateView):
    """
    View that handles the post from the preview form and submits it.
    """

    success_url = "/blog/"

    #Do front end validation too....

    def form_invalid(self, form):
        #If this form is invalid something is very wrong.  We we log it redirect the user for now...
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        slug = ""
        if request.session._session['form'].cleaned_data['slug']:
            slug = request.session._session['form'].cleaned_data['slug']
        data = {'title': request.session._session['form'].cleaned_data['title'],
                'published':request.session._session['form'].cleaned_data['published'],
                'author':request.session._session['form'].cleaned_data['author'].id,
                'content':request.session._session['form'].cleaned_data['content'],
                'slug': slug
        }
        qdict = QueryDict('')
        qdict = qdict.copy()
        qdict.update(data)
        if request.session._session['form'].cleaned_data['clearPhoto']:
            form = PostFinalForm(data)
        else:
            form = PostFinalForm(data, MultiValueDict({'photo': [request.session._session['form'].cleaned_data['photo']]}))
        #request.session.flush()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)