from django.conf.urls import patterns, url

from .views import SurmandlUserView, SurmandlUserPasswordChangeView

urlpatterns = patterns('',
                       url(r'^$', SurmandlUserView.as_view(), name="user"),
                       url(r'^password_change/$', SurmandlUserPasswordChangeView.as_view(), name="password_change")
                       )