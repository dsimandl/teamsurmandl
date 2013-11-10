from django.db import models
from django.template.defaultfilters import slugify
from profiles.admin import SurmandlUser

class PostManager(models.Manager):

    def live(self):
        return self.model.objects.filter(published=True)

class Post (models.Model):

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField('Blog title', max_length=255)
    slug = models.SlugField(max_length=255, blank=True, default='')
    content = models.TextField('Blog post content')
    published = models.BooleanField(default=True)
    photo = models.ImageField('Photo for blog post', upload_to='blog', blank=True)
    author = models.ForeignKey(SurmandlUser, limit_choices_to={'is_staff':True},related_name='posts', verbose_name='Author for blog posts')

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('blog:detail', (), {'slug':self.slug})

class PostComment(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    content = models.TextField()
    author = models.ForeignKey(SurmandlUser, related_name='user_comments')
    post = models.ForeignKey(Post, related_name='user_post')

    def __unicode__(self):
        return self.content

