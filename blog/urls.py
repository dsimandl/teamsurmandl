"""blog specific url routing file """
from django.conf.urls import patterns, url
from .views import PostListView, PostDetailView, PostTagIndexView

urlpatterns = patterns('',
                       url(r'^$', PostListView.as_view(), name="list"),
                       url(r'^(?P<slug>[\w-]+)$', PostDetailView.as_view(), name="edit"),
                       url(r'^tag/(?P<slug>[-\w]+)/$', PostTagIndexView.as_view(), name="tagged"),
)
