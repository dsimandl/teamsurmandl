from django.core.urlresolvers import resolve
from django.test import TestCase
from teamsurmandl.views import LoginView

class LoginPageTest(TestCase):

    def test_root_url_resolves_to_logon_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func.func_name, LoginView.__name__)