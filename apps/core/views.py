import imp
from re import template
from django.shortcuts import render
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'core/index.html'


class Signup(TemplateView):
    template_name = 'core/signup.html'
