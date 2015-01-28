from django.core.urlresolvers import resolve
from django.test import TestCase
from teamsurmandl.views import LoginView
from profiles.models import SurmandlUser

class LoginPageTest(TestCase):
    def test_root_url_resolves_to_logon_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func.func_name, LoginView.__name__)

    def test_login_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, 'Team Surmandl!')


class HomePageTest(TestCase):
    def test_home_page_login(self):
        self.user = SurmandlUser.objects.create_user('test@test.com', 'test', 'user', 'self', password='Passw0rd')
        self.client.login(username='', password='')
        self.assertFalse(self.client.session)
        self.client.login(username='test@test.com', password='')
        self.assertFalse(self.client.session)
        self.client.login(username='', password='Passw0rd')
        self.assertFalse(self.client.session)
        self.client.login(username='test@test.com', password='Test')
        self.assertFalse(self.client.session)
        self.client.login(username='test@test.com', password='Passw0rd')
        self.assertTrue(self.client.session)




