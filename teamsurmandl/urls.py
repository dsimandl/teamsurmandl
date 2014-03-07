from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


from teamsurmandl.views import LoginView, HomePageView, LogOutView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', LoginView.as_view(), name="login"),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^logout/', LogOutView.as_view(), name="logout"),
    url(r'^home/', HomePageView.as_view(), name="Home"),
    url(r'^blog/', include("blog.urls", namespace="blog"), name="blog"),
    url(r'^profile/', include("profiles.urls", namespace="profile"), name="profile"),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),

)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT
    }),
    )

