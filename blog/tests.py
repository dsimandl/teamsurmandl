from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from model_mommy import mommy

from .models import Post, PostComment

class BlogBasicTest(TestCase):
    """Basic test class to test the fields, the saving of the slug, a custom slug, and the model manager
    """


    def setUp(self):

        self.new_post = mommy.make(Post)
        self.new_comment = mommy.make(PostComment)

    def test_post_create(self):

        self.assertTrue(isinstance(self.new_post, Post))
        self.assertEqual(self.new_post.__unicode__(), self.new_post.title)
        self.assertEqual(reverse('blog:edit', kwargs={'slug': self.new_post.slug}), self.new_post.get_absolute_url())


    def test_post_comment_create(self):
        self.assertTrue(isinstance(self.new_comment, PostComment))
        self.assertEqual(self.new_comment.__unicode__(), self.new_comment.comment)
  #  def test_slug_on_save(self):

  #      self.assertEqual(self.post.slug, 'make-more-tests')

    def test_model_manager(self):
        live_post = self.new_post
        draft_post = self.new_post.published=False
        self.assertIn(live_post, Post.objects.live())
        self.assertNotIn(draft_post, Post.objects.live())

#    def test_custom_slug(self):
#        post = Post.objects.create(
#            title='A Post with a Custom Slug',
#            slug='fizzbuzz',
#            author=self.user
#        )
#        self.assertNotEqual(post.slug, slugify(post.title))
#        self.assertEqual(post.slug, 'fizzbuzz')