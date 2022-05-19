from django.db import models
from django.conf import settings
from pypaystack import Transaction as PaystackTx
import datetime
import random
from ..customer.models import Customer, Job

# Create your models here.


class Block(models.Model):
    date = models.DateField(auto_now_add=True, unique=True)

    def __str__(self) -> str:
        return str(self.date)


class Transaction(models.Model):
    STATUS_OPTIONS = (
        ('0', 'pending'),
        ('1', 'approved'),
        ('2', 'declined'),
    )

    PAY_METHOD_OPTIONS = (
        ('0', 'USSD'),
        ('1', 'Card'),
    )

    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, related_name='transactions')
    job = models.OneToOneField(
        Job, on_delete=models.SET_NULL, null=True, related_name='transaction_info')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    ref = models.CharField(max_length=14, blank=True)
    status = models.CharField(
        max_length=2, choices=STATUS_OPTIONS, default=STATUS_OPTIONS[0][0])
    payment_method = models.CharField(max_length=2, choices=PAY_METHOD_OPTIONS)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def pretty_ref(self) -> str:
        """
        A property to return transaction
        ref in a prettified format of
        P-YYYY-MM-DD-XXXXX
        """
        base_code = self.ref
        pretty_code = ""
        for idx, _ in enumerate(base_code):
            if idx == 0 or idx == 4 or idx == 6 or idx == 8:
                pretty_code += (base_code[idx] + '-')
            else:
                pretty_code += base_code[idx]
        return pretty_code

    def verify_payment(self) -> bool:
        # for USSD payment verification
        if self.payment_method == '0':
            status = False
            if self.status == '1':
                status = True
                # TODO: Notify the admin to confirm cash transfer
        # for card payment verificaton
        elif self.payment_method == '1':
            status = False
            transaction = PaystackTx(
                authorization_key=settings.PAYSTACK_SECRET_KEY)
            status_code, status, message, data = transaction.verify(
                self.ref)
            if status_code == 200:
                if status:
                    self.payment_status = self.STATUS_OPTIONS[1][0]
                    status = True
                else:
                    self.payment_status = self.STATUS_OPTIONS[2][0]
                self.save()
        return status

    def _generate_ref(self) -> str:
        code = "P"
        current_date = datetime.date.today()
        code += str(current_date.year)
        code += self._prepend_zero(str(current_date.month))
        code += self._prepend_zero(str(current_date.day))
        code += self._generate_random()
        return code

    def generate_ref(self) -> str:
        """
        Generates a transaction reference code.
        in the format.
        PYYYYMMDDXXXXX
        """
        code = self._generate_ref()
        # prevent the existence of two transactions with the same ref.
        while Transaction.objects.filter(ref=code).count() >= 1:
            code = self._generate_ref()
        return code

    def _prepend_zero(self, value: str, length: int = 2) -> str:
        """
        Appends zeros to the start of a value if 
        it is less than the required length
        """
        final_value = value
        while len(final_value) < length:
            final_value = '0' + final_value
        return final_value

    def _generate_random(self, length: int = 5) -> str:
        result = ""
        while len(result) < length:
            result += str(random.randint(0, 9))
        return result

    def save(self, *args, **kwargs) -> None:
        if self.ref is None or self.ref == "":
            self.ref = self.generate_ref()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.pretty_ref
