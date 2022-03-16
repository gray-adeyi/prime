from django.test import SimpleTestCase
from django.urls import resolve, reverse
from .. import views


class TestUrls(SimpleTestCase):

    def test_url_login_works(self):
        url = reverse('editor:login')
        self.assertEquals(resolve(url).func, views.login_editor)

    def test_editor_dasboard_url_works(self):
        url = reverse("editor:dashboard")
        self.assertEqual(resolve(url).func.view_class, views.Dashboard)

    def test_editor_logout_url_works(self):
        url = reverse("editor:logout")
        self.assertEquals(resolve(url).func, views.logout_editor)
