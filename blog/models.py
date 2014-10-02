from django.db import models
from django.template.defaultfilters import slugify

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager

from profiles.admin import SurmandlUser

class PostManager(models.Manager):
    """
    Simple model manager to make sure we only query published blog posts
    """

    def live(self):
        return self.model.objects.filter(published=True)

class Post (models.Model):
    """
    The post model.  We have a tag object to use for post tagging.
    We override the save method to slugify the title for our slug.  We also make sure the primary key of the post isn't null because of the current preview functionality
    We also order by the created_by field
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField('Blog title', max_length=255)
    slug = models.SlugField(max_length=255, blank=True, default='')
    content = models.TextField('Blog post content')
    published = models.BooleanField(default=True)
    photo = ProcessedImageField(upload_to='blog', processors=[ResizeToFill(400, 300)], format='JPEG', options={'quality': 60}, verbose_name='Photo for blog post', blank=True)
    author = models.ForeignKey(SurmandlUser, limit_choices_to={'is_staff':True},related_name='posts', verbose_name='Author for blog posts')

    tags = TaggableManager(blank=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('blog:edit', (), {'slug':self.slug})

    class Meta:
        ordering = ['created_at']




class PostComment(models.Model):
    """
    Fairly standard model for the post comments, linked to each post
    """

    created_at = models.DateTimeField(verbose_name='Comment created at',auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    comment = models.TextField('Comment')
    author = models.ForeignKey(SurmandlUser, related_name='user_comments', verbose_name='Comment author')
    post = models.ForeignKey(Post, related_name='user_post')

    def __unicode__(self):
        return self.comment

