from django.shortcuts import render
from django.views.generic import TemplateView


class Login(TemplateView):
    template_name = 'customer/login.html'
