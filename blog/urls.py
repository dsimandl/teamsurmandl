"""blog specific url routing file """
from django.conf.urls import patterns, url, include

from .views import PostListView, PostDetailView, PostTagIndexView, PostTitleIndexView, delete_comment
from .api import PostResource

post_resource = PostResource()

urlpatterns = patterns('',
                       url(r'^$', PostListView.as_view(), name="list"),
                       url(r'^search/$', PostTitleIndexView.as_view(), name="search"),
                       url(r'^(?P<slug>[\w-]+)$', PostDetailView.as_view(), name="edit"),
                       url(r'^tag/(?P<slug>[-\w]+)/$', PostTagIndexView.as_view(), name="tagged"),
                       url(r'^delete/(?P<id>[0-9]+)/$', delete_comment, name="delete"),
                       url(r'^api/', include(post_resource.urls )),
)
