from django.conf.urls import patterns, url

from .views import CurrentLocation, PastLocations

urlpatterns = patterns('',
                       url(r'^current_location/$', CurrentLocation.as_view(), name="current_location"),
                       url(r'^past_locations/$', PastLocations.as_view(), name="past_locations"),
                       )