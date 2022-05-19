from django.views.generic import TemplateView
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib import messages
from . import forms


def login_editor(request):
    template_name = "editor/login.html"
    if request.method == "GET":
        return render(request, template_name, {"form": forms.LoginForm()})
    elif request.method == "POST":
        new_login = forms.LoginForm(request.POST)
        if new_login.is_valid():
            user = authenticate(username=new_login.get_username(
                login_id=new_login.cleaned_data['login_id']), password=new_login.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect("editor:dashboard")
            else:
                messages.error(request, "Your account has been deactivated")
                return redirect("editor:login")
        else:
            return render(request, template_name, {"form": new_login})
    else:
        return HttpResponseNotAllowed(
            ["POST", "GET"]
        )


def logout_editor(request):
    login(request)
    return redirect("editor:login")


class Dashboard(TemplateView):
    template_name = "editor/dashboard.html"
