from django.conf.urls import patterns, url

from blog.views import PostListView, PostDetailView, PostEditView

urlpatterns = patterns('',
                       url(r'^$', PostListView.as_view(), name="list"),
                       url(r"^edit/(?P<pk>\d+)$", PostEditView, name="edit_post"),
                       url(r"^(?P<slug>[\w-]+)$", PostDetailView.as_view(), name="detail"),
)
