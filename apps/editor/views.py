from django.views.generic import TemplateView
from django.http import HttpResponseNotAllowed
from django.shortcuts import render


def login_editor(request):
    template_name = "editor/login.html"
    if request.method == "GET":
        return render(request, template_name,)
    elif request.method == "POST":
        pass
    else:
        return HttpResponseNotAllowed(
            ["POST", "GET"]
        )
