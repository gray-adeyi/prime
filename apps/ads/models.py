from django.db import models

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='client/logo/images')
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Ads(models.Model):
    models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    expiry_timestamp = models.DateField()

    class Meta:
        verbose_name_plural = 'Ads'


class Poster(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='poster/image/images')
