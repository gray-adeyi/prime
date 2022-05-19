from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from . import models

# TODO: Package pypaystack in the root seperately.


class CardPay(View):
    def get(self, request) -> HttpResponse:
        tx = None  # TODO: Retrieve the appropriate transaction.
        return render(request, 'finance/card-pay.html', {'tx', tx})


class ConfrimPay(View):

    def get(self, request: HttpRequest, tx_id: str) -> HttpResponse:
        template_name = "finance/confirm-pay.html"
        ctx = {"payment_status": False}
        txn = models.Transaction.objects.get(ref=tx_id)
        payment_status = txn.verify_payment()
        if payment_status:
            ctx["payment_status"] = True
        return render(request, template_name, ctx)
