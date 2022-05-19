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


class BankInformations(models.Model):
    BANK_OPTIONS = (
        ('uba', 'UBA'),
        ('fcmb', 'FCMB'),
        ('sterling', 'STERLING BANK'),
        ('kuda', 'KUDA MFB'),
        ('gtb', 'GTB'),
    )
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name='bank_infos')
    bank = models.CharField(max_length=20, choices=BANK_OPTIONS)
    account_name = models.CharField(max_length=25)
    account_number = models.CharField(max_length=14,)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.account_name
