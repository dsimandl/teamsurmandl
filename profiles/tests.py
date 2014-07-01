from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import SurmandlUser

from model_mommy import mommy

class UserBasicTest(TestCase):

    def setUp(self):

        self.new_user = mommy.make(SurmandlUser)

    def test_user_create(self):

        self.assertTrue(isinstance(self.new_user, SurmandlUser))
        self.assertEqual(self.new_user.__unicode__(), "%s %s" % (self.new_user.first_name, self.new_user.last_name))
        self.assertEqual(self.new_user.get_short_name(), self.new_user.email)
        self.assertEqual(self.new_user.get_full_name(), "%s, %s %s" % (self.new_user.email,
                                                                       self.new_user.first_name, self.new_user.last_name))

    def test_user_manager(self):

        manager_user = SurmandlUser.objects.create_user('test@test.com', 'test', 'user', 'self', '12345')
        self.assertEqual(manager_user.email, 'test@test.com')
        self.assertEqual(manager_user.first_name, 'test')
        self.assertEqual(manager_user.last_name, 'user')
        self.assertEqual(manager_user.relation, 'self')

    def test_empty_email_address(self):
        self.assertRaisesMessage(
            ValueError,
            'Users must have a valid email address',
            SurmandlUser.objects.create_user, email='', first_name='test', last_name='user', relation='self'
        )

    def test_super_user_manager(self):

        super_manager_user = SurmandlUser.objects.create_superuser('super@test.com', 'super', 'user', 'self', '1234')
        self.assertEqual(super_manager_user.email, 'super@test.com')
        self.assertEqual(super_manager_user.first_name, 'super')
        self.assertEqual(super_manager_user.last_name, 'user')
        self.assertEqual(super_manager_user.relation, 'self')


