from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.http.response import HttpResponseForbidden
from teamsurmandl.views import LoginView

class LoginPageTest(TestCase):

    def test_root_url_resolves_to_logon_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func.func_name, LoginView.__name__)

    def test_login_page_returns_correct_html(self):
        request = HttpRequest()
        response = LoginView.as_view()(request)
        self.assertTrue(isinstance(response, HttpResponseForbidden))
