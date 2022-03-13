from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms


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
    return redirect('customer:login')


class Dashboard(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('customer:login')
    template_name = 'customer/dashboard.html'
