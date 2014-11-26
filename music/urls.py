from django.conf.urls import patterns, url

from .views import MusicView

urlpatterns = patterns('',
                       url(r'^(?P<first_name>\w+)/$', MusicView.as_view(), name="music"),
                       )