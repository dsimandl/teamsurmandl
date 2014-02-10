from django.conf.urls import patterns, url
from django.views.decorators.http import require_POST

from .views import PostListView, PostEditView, PostCreateView, PostPreviewView, HiddenFormView, PostTagIndexView

urlpatterns = patterns('',
                       url(r'^$', PostListView.as_view(), name="list"),
                       url(r'^tag/(?P<slug>[-\w]+)/$', PostTagIndexView.as_view(), name="tagged"),
                       url(r'^create/$', PostCreateView.as_view(), name='create_post'),
                       url(r'^preview/$', PostPreviewView.as_view(), name='preview_post'),
                       url(r'^final/$', require_POST(HiddenFormView.as_view()), name='final_create'),
                       url(r'^(?P<slug>[\w-]+)$', PostEditView.as_view(), name='detail'),
)
