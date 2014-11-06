from django.conf.urls import patterns, url

from .views import MusicView

urlpatterns = patterns('',
                       url(r'^$', MusicView.as_view(), name="music"),
                       )