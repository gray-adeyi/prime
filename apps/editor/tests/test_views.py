from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .. import models


class TestViews(TestCase):
    def test_editor_can_login(self):
        user_data = {
            "username": "jigani",
            "email": "coyotedevmail@gmail.com",
            "is_active": True,
        }
        payload = {
            "login_id": "coyotedevmail@gmail.com",
            "password": "iLoveRice99"
        }
        user = User.objects.create(**user_data)
        user.set_password("iLoveRice99")
        user.save()
        self.assertTrue(user.check_password("iLoveRice99"))
        self.assertEquals(User.objects.all().count(), 1)
        editor = models.Editor.objects.create(user=user)
        client = Client()
        response = client.post(reverse("editor:login"), data=payload)
        self.assertRedirects(response, reverse(
            "editor:dashboard"), status_code=302, target_status_code=200)
