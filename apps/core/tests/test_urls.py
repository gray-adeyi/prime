from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import Index, Signup


class TestURLs(SimpleTestCase):
    def test_index_url_is_resolves(self):
        url = reverse('core:index')
        self.assertEquals(resolve(url).func.view_class, Index)

    def test_signup_url_resolves(self):
        url = reverse('core:signup')
        self.assertEquals(resolve(url).func.view_class, Signup)
