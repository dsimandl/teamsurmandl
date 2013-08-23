from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from teamsurmandl.views import HomePageView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name="login"),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^static/(.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),
)
