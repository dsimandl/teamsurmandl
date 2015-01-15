from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.http.response import HttpResponseForbidden
from music.views import MusicView

class MusicPageTest(TestCase):

    def test_root_url_resolves_to_logon_page_view(self):
        found = resolve('/music')
        self.assertEqual(found.func.func_name, MusicView.__name__)

    def test_login_page_returns_correct_html(self):
        request = HttpRequest()
        response = MusicView.as_view()(request)
        self.assertTrue(isinstance(response, HttpResponseForbidden))