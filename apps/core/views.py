import django


from django.http import HttpResponse, HttpResponseRedirect
from re import template
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib import messages
import enum
from . import forms
from ..editor import models as emods
from ..customer import models as cmods


class ValidationMode(enum.Enum):
    """
    The ValidationMode enum helps
    to condition user sign up 
    validation into two modes.
    In the Implicit mode,
    email validation is used
    to validate users While
    in the Explicit mode, An
    admin is requied to validate
    a user before they get access
    to their accounts.
    """
    Implicit = 0
    Explicit = 1


VALIDATION_MODE = ValidationMode.Implicit


class Signup(FormView):
    form_class = forms.SignupForm
    template_name = 'core/signup.html'

    def form_valid(self, form: forms.SignupForm) -> HttpResponse:
        if form.cleaned_data['user_type'] == '0':
            self.signup_photographer(form)
            # choose redirect path based on Validation mode.
            if VALIDATION_MODE == ValidationMode.Implicit:
                form.sendmail()
                messages.success(
                    self.request, f"Dear {form.cleaned_data['username']}, your account has been created but you'll need to activate it from the email we just sent to you before you can login")
                return redirect('customer:login')
            else:
                messages.success(
                    self.request, f"Dear {form.cleaned_data['username']}, you account has been created")
                messages.warning(
                    self.request, "The admin still has to authorize you before you can login.")
                return redirect('customer:login')
        elif form.cleaned_data['user_type'] == '1':
            self.signup_editor(form)
            messages.success(
                self.request, f"Dear {form.cleaned_data['username']}, your account has been created.")
            messages.warning(
                self.request, f"You'll be unable to login at the moment as you'll need the admin to authorize you. please bear with us, you'll receive a message soon.")
            # redirect to editor login
            return redirect('editor:login')
        messages.error(self.request, 'Unknown user type. Try again')
        return redirect('core:signup')

    def form_invalid(self, form: forms.SignupForm) -> HttpResponse:
        return super().form_invalid(form)

    def _create_user(self, form: forms.SignupForm) -> User:
        """
        Creates and returns a User instance
        """
        new_user = User.objects.create(username=form.cleaned_data['username'],
                                       email=form.cleaned_data['email'],
                                       is_active=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return new_user

    def signup_editor(self, form: forms.SignupForm):
        """
        Signs up the user as an editor
        """
        user = self._create_user(form)
        emods.Editor.objects.create(user=user)

    def signup_photographer(self, form: forms.SignupForm):
        """
        Signs up the user as a photographer
        """
        user = self._create_user(form)
        cmods.Customer.objects.create(user=user)


class Index(TemplateView):
    template_name = 'core/index.html'


class About(TemplateView):
    template_name = 'core/about.html'
