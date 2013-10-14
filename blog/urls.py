from django.conf.urls import patterns, url

from .views import PostListView, PostDetailView, PostEditView, PostCreateView

urlpatterns = patterns('',
                       url(r'^$', PostListView.as_view(), name="list"),
                       url(r'^create/$', PostCreateView.as_view(), name='create_post'),
                       url(r"^edit/(?P<pk>\d+)$", PostEditView.as_view(), name="edit_post"),
                       url(r"^(?P<slug>[\w-]+)$", PostDetailView.as_view(), name="detail"),
)
