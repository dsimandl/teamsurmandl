from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from .models import Post

from .models import SurmandlUser

class BlogBasicTest(TestCase):


    def setUp(self):

        self.user = SurmandlUser()
        self.user.id = '676'
        self.user.email = "test@test.com"
        self.user.first_name = "test"
        self.user.last_name = "user"
        self.user.relation = "self"

        self.post = Post()
        self.post.title = "Make more Tests"
        self.post.content = "This is a test post"
        self.post.author = self.user
        self.post.author_id = self.user.id
        self.post.save()


    def test_fields(self):

        post = Post()
        post.title = "This is the first test!"
        post.content = "This is a test post.  More of these will be made"
        post.author = self.user
        post.author_id = self.user.id
        post.save()

        record = Post.objects.get(pk=post.id)
        self.assertEqual(record, post)

    def test_slug_on_save(self):

        self.assertEqual(self.post.slug, 'make-more-tests')

    def test_get_absolute_url(self):

        #The reverse gets us our application instance name (aka, the namespace which in this case is blog)
        self.assertEqual(
            self.post.get_absolute_url(),
            reverse('blog:detail', kwargs={'slug': self.post.slug})
        )

    def test_model_manager(self):
        live_post = self.post
        draft_post = self.post.published=False
        self.assertIn(live_post, Post.objects.live())
        self.assertNotIn(draft_post, Post.objects.live())

    def test_custom_slug(self):
        post = Post.objects.create(
            title='A Post with a Custom Slug',
            slug='fizzbuzz',
            author=self.user
        )
        self.assertNotEqual(post.slug, slugify(post.title))
        self.assertEqual(post.slug, 'fizzbuzz')