from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .. import models
from apps import customer


class TestViews(TestCase):

    def test_customer_can_login(self):
        user = User.objects.create(
            email="coyotedevmail@gmail.com",
            username="jigani",
            is_active=True
        )
        user.set_password('iLoveRice')
        user.save()
        self.assertTrue(user.check_password('iLoveRice'))
        customer = models.Customer.objects.create(user=user)
        client = Client()
        login_credentials = {
            'login_id': 'jiganidd',
            'password': 'iLoveRice'
        }
        response = client.post(reverse('customer:login'),
                               data=login_credentials)
        # self.assertRedirects(response, reverse('customer:dashboard'), 302)
        self.assertFormError(response, 'form', 'login_id', 'lol')
