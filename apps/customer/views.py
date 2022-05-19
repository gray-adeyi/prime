import datetime
from io import BytesIO
import os
from django.contrib import messages
from typing import List, Any, Dict
import zipfile
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
import tempfile
from PIL import Image
import random
from . import forms, models
from apps.finance import models as fm
from apps import customer

# TODO: clean up job picture files when instance is deleted.


def login_customer(request):
    template_name = 'customer/login.html'
    if request.method == "GET":
        return render(request, template_name, {'form': forms.LoginForm()})
    elif request.method == "POST":
        new_login = forms.LoginForm(request.POST)
        if new_login.is_valid():
            # Authentication is running twice. first in the forms clean method and now.
            user = authenticate(
                username=new_login.get_username(new_login.cleaned_data['login_id']), password=new_login.cleaned_data['password'])
            login(request, user)
            # Redirect customer to customer dashboard
            return redirect('customer:dashboard')
        else:
            return render(request, template_name, {'form': new_login})
    return HttpResponseNotAllowed([
        'POST',
        'GET',
    ])


def logout_customer(request):
    logout(request)
    messages.success(
        request, "Sign out successful. It was lovely having you around. Can't wait to see you again.")
    return redirect('customer:login')


class Dashboard(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('customer:login')
    template_name = 'customer/dashboard.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['customer'] = models.Customer.objects.get(
            user=self.request.user)
        context['pending_jobs'] = models.Job.objects.filter(
            customer=context['customer'],
            status=models.Job.STATUS_OPTIONS[0][0])
        context['processing_jobs'] = models.Job.objects.filter(
            customer=context['customer'],
            status=models.Job.STATUS_OPTIONS[1][0])
        return context


def rand_str(length: int = 6) -> str:
    """
    Returns a random string of the provided length
    """
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ0123456789"
    result = ""
    while len(result) < length:
        result += chars[random.randint(0, len(chars)-1)]
    return result


def download_job(request: HttpRequest, job_id):
    job = models.Job.objects.get(id=job_id)
    with tempfile.TemporaryDirectory() as tdir:
        for exposure in job.exposures.all():
            if exposure.copies > 1:
                with open(f'{tdir}/{exposure.copies}-copies-{rand_str()}.{os.path.splitext(exposure.image.name)[1]}', 'wb') as f:
                    image = Image.open(exposure.image)
                    image = image.convert('RGB')
                    data = BytesIO()
                    image.save(data)
                    data.seek(0)
                    f.write(data.read())
            else:
                with open(f'{tdir}/{exposure.image.name}', 'wb') as f:
                    image = Image.open(exposure.image)
                    image = image.convert('RGB')
                    data = BytesIO()
                    image.save(data)
                    data.seek(0)
                    f.write(data.read())

        images_list = os.listdir(f"{tdir}")
        with zipfile.ZipFile(f"{tdir}/{job.customer.user.username}.zip", mode='w') as zf:
            for file in images_list:
                zf.write(f"{file}")
                # zf.write(f"{tdir}/{file}")

        response = HttpResponse(
            content_type="application/zip, application/octet-stream"
        )
        response["Content-Disposition"] = f"inline; filename={job.customer.user.username}.zip"
        response["Content-Transfer-Encoding"] = "binary"
        with open(f"{tdir}/{job.customer.user.username}.zip", 'rb') as f:
            response.write(f.read())
        return response


def book_job(request: HttpRequest):
    return render(request, 'customer/partials/book-job.html')


def create_new_booking(request: HttpRequest):

    def new_booking(picture_files: List[str]) -> models.Job:
        customer = models.Customer.objects.get(user=request.user)
        new_job = models.Job.objects.create(
            customer=customer, copies=len(picture_files))
        for _file in picture_files:
            new_job.exposures.create(image=_file)

        return new_job

    if request.method == "POST":
        job_form = forms.BookJobForm(request.POST, request.FILES)
        picture_files = request.FILES.getlist('picture_files')
        if job_form.is_valid():
            job = new_booking(picture_files)
            if request.POST.get('write_up') != '':
                job.write_up = request.POST.get('write_up')
                job.save()
            return render(request, 'customer/partials/bookings.html', {'job': job})
        else:
            return HttpResponse("<h2>An error occured and it's our fault. Please refesh your browser and try again.</h2>")


def confirm_discard(request: HttpRequest, job_id: int):
    job = models.Job.objects.get(id=job_id)
    return render(request, 'customer/partials/confirm-discard.html', {'job': job})


def discard_booking(request: HttpRequest, job_id: int):
    models.Job.objects.get(id=job_id).delete()
    return HttpResponse("<h3>Successfully deleted</h3>")


def inc_exposure(request: HttpRequest, id: int):
    exposure = models.Photo.objects.get(id=id)
    job = exposure.job
    exposure.copies += 1
    exposure.save()
    return render(request, 'customer/partials/bookings.html', {'job': job})


def dec_exposure(request: HttpRequest, id: int):
    exposure = models.Photo.objects.get(id=id)
    job = exposure.job
    if exposure.copies > 1:
        exposure.copies -= 1
        exposure.save()
    return render(request, 'customer/partials/bookings.html', {'job': job})


def del_exposure(request: HttpRequest, id: int):
    exposure = models.Photo.objects.get(id=id)
    job = exposure.job
    exposure.delete()
    return render(request, 'customer/partials/bookings.html', {'job': job})


def pending_jobs(request: HttpRequest):
    customer = models.Customer.objects.get(
        user=request.user)
    pending_jobs = models.Job.objects.filter(
        customer=customer,
        status=models.Job.STATUS_OPTIONS[0][0])
    return render(request, 'customer/partials/pending-jobs.html', {'pending_jobs': pending_jobs})


def show_pending_jobs(request: HttpRequest, id: int):
    job = models.Job.objects.get(id=id, customer__user=request.user)
    return render(request, 'customer/partials/bookings.html', {'job': job})


def pay_methods(request: HttpRequest, id: int):
    return render(request, 'customer/partials/pay-methods.html', {'job_id': id})


def transfer_and_verify(request: HttpRequest, job_id: int):
    job = models.Job.objects.get(customer__user=request.user, id=job_id)
    block, _ = fm.Block.objects.get_or_create(date=datetime.date.today())
    tx, _ = fm.Transaction.objects.get_or_create(customer=job.customer, block=block, job=job,
                                                 amount=job.total_price, payment_method=fm.Transaction.PAY_METHOD_OPTIONS[0][0])
    return render(request, 'customer/partials/transfer-and-verify-cash-transfer.html', {'job': job})
