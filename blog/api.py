from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication
from tastypie.constants import ALL

from .models import Post, PostComment

class PostResource(ModelResource):

    class Meta:
        queryset = Post.objects.all()
        resource_name = 'post'
        filtering = {"title": ALL}

        authentication = SessionAuthentication()