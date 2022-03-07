from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=50, blank=True)
    logo = models.ImageField(upload_to='customer/logo/images', blank=True)

    def __str__(self) -> str:
        return self.business_name if self.business_name is not None else self.user.firstname


class Job(models.Model):

    # TODO: Add more job type options
    JOB_TYPE_OPTIONS = (
        (0, '4x6'),
        (1, '5x7'),
        (2, '8x10')
    )

    STATUS_OPTIONS = (
        (0, 'processing'),
        (1, 'completed')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    copies = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=8, decimal_places=2)
    job_type = models.CharField(max_length=2, choices=JOB_TYPE_OPTIONS)
    status = models.CharField(max_length=2, choices=STATUS_OPTIONS)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.customer} job @ {self.timestamp}"
