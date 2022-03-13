from http import client
from urllib import response
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps import customer
from apps.customer import models as cmods
from apps.editor import models as emods
from .. import forms


class TestViews(TestCase):
    def setUp(self):
        self.customer_payload = {
            'username': 'jigani',
            'email': 'coyotedevmail@gmail.com',
            'password': '123',
            'confirm_password': '123',
            'user_type': '0',
        }

        self.editor_payload = {
            'username': 'jigani',
            'email': 'coyotedevmail@gmail.com',
            'password': '123',
            'confirm_password': '123',
            'user_type': '1',
        }

    def test_index_view_uses_the_right_template(self):
        response = Client().get(reverse('core:index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_signup_view_uses_the_right_template(self):
        response = Client().get(reverse('core:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')

    def test_signup_view_signs_up_customer(self):
        client = Client()
        response = client.post(reverse('core:signup'),
                               data=self.customer_payload)
        # TODO: Confirm that the status code for success post is 302
        self.assertEquals(response.status_code, 302)
        user = User.objects.get(email=self.customer_payload['email'])
        self.assertFalse(user.is_active)
        cmods.Customer.objects.get(user=user)
        customers_count = cmods.Customer.objects.all().count()
        self.assertEquals(customers_count, 1)

    def test_signup_view_signs_up_editor(self):
        client = Client()
        response = client.post(reverse('core:signup'),
                               data=self.editor_payload)
        # TODO: Confirm that the status code for success post is 302
        self.assertEquals(response.status_code, 302)
        user = User.objects.get(email=self.editor_payload['email'])
        self.assertFalse(user.is_active)
        emods.Editor.objects.get(user=user)
        editors_count = emods.Editor.objects.all().count()
        self.assertEquals(editors_count, 1)

    def test_signup_customer_fails_on_user_already_exists(self):
        user = User.objects.create(
            email="coyotedevmail@gmail.com", is_active=False)
        customer = cmods.Customer.objects.create(user=user)
        response = Client().post(reverse('core:signup'), data=self.customer_payload)
        self.assertFormError(response, 'form',
                             'email', ['User with this email already exist. Please sign up with another email or sign in with the existing account'])
        users_count = User.objects.all().count()
        self.assertEquals(users_count, 1)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')

    def test_signup_editor_fails_on_user_already_exists(self):
        user = User.objects.create(
            email="coyotedevmail@gmail.com", is_active=False)
        customer = emods.Editor.objects.create(user=user)
        response = Client().post(reverse('core:signup'), data=self.editor_payload)
        self.assertFormError(response, 'form',
                             'email', ['User with this email already exist. Please sign up with another email or sign in with the existing account'])
        users_count = User.objects.all().count()
        self.assertEquals(users_count, 1)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')
