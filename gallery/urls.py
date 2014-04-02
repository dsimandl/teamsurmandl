from django.conf.urls import patterns, url

from .views import AlbumView

urlpatterns = patterns('',
                       url(r'^$', AlbumView.as_view(), name="album"),
                       )