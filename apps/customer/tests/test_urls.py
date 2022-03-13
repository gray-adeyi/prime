from django.urls import reverse, resolve
from django.test import SimpleTestCase
from .. import views


class TestURLs(SimpleTestCase):
    def test_cutomer_login_url(self):
        url = reverse('customer:login')
        self.assertEquals(resolve(url).func, views.login_customer)

    def test_customer_logout_url(self):
        url = reverse('customer:logout')
        self.assertEquals(resolve(url).func, views.logout_customer)

    def test_customer_dashboard_url(self):
        url = reverse('customer:dashboard')
        self.assertEquals(resolve(url).func.view_class, views.Dashboard)
