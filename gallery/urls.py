from django.conf.urls import patterns, url

from .views import AlbumView, AlbumListView, SlideShowView

urlpatterns = patterns('',
                       url(r'^$', AlbumView.as_view(), name="album"),
                       url(r'images/(?P<album_id>\d+)/$', AlbumListView.as_view(), name="images"),
                       # Add album ID as well to the url to pull up the images JUST for the album.  The Album is
                       # Is still the top level
                       url(r'image_show/(?P<image_id>\d+)/(?P<album_id>\d+)/$',
                           SlideShowView.as_view(), name="images_show"),
                       )