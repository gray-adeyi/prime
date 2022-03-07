from django.db import models
from ..customer.models import Customer

# Create your models here.


class Block(models.Model):
    date = models.DateField()


class Transaction(models.Model):
    STATUS_OPTIONS = (
        (0, 'pending'),
        (1, 'approved'),
        (2, 'declined'),
    )

    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=2, choices=STATUS_OPTIONS)
    timestamp = models.DateTimeField(auto_now_add=True)
