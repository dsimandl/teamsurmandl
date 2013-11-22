from django.conf.urls import patterns, url

from .views import PostListView, PostEditView, PostCreateView

urlpatterns = patterns('',
                       url(r'^$', PostListView.as_view(), name="list"),
                       url(r'^create/$', PostCreateView.as_view(), name='create_post'),
                       url(r'^(?P<slug>[\w-]+)$', PostEditView.as_view(), name='detail'),
)
