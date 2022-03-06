from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Editor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='editor/profile_picture/images')

    def __str__(self) -> str:
        return self.user.firstname
