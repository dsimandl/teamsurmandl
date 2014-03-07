from django.conf.urls import patterns, url

from .views import SurmandlUserView

urlpatterns = patterns('',
                       url(r'^$', SurmandlUserView.as_view(), name="user"),
                       )