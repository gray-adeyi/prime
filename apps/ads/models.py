from distutils.command.upload import upload
from django.db import models

# Create your models here.


class Site(models.Model):
    """
    Model holds website data.
    """
    name = models.CharField(max_length=50)
    favion = models.ImageField(upload_to='site/favicon/images')
    appleicon = models.ImageField(upload_to='site/appleicon/images')
    logo = models.ImageField(upload_to='site/logo/images')

    def __str__(self) -> str:
        return self.name
