from django.conf.urls import patterns, url

from .views import AlbumView, SlideShowView

urlpatterns = patterns('',
                       url(r'^$', AlbumView.as_view(), name="album"),
                       url(r'image/(?P<album_id>\d+)/$', SlideShowView.as_view(), name="images"),
                       )