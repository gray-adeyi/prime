from random import choices
from typing import Optional, Any, Mapping
from secrets import choice
from urllib import request
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# TODO: Ensure that the user
# does not already exist.
class SignupForm(forms.Form):
    USER_TYPE_OPTIONS = (
        (0, 'Customer (Photographer)'),
        (1, 'Editor'),
    )
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        max_length=128, widget=forms.PasswordInput)
    user_type = forms.CharField(
        max_length=1, widget=forms.RadioSelect(choices=USER_TYPE_OPTIONS))

    def sendmail(self):
        """
        Sends an emal to the user
        to activate their account
        """
        pass

    def clean(self) -> Optional[Mapping[str, Any]]:
        cleaned_data = super().clean()
        self._validate_user_with_supplied_email_exits(cleaned_data['email'])
        self._validate_user_with_supplied_username_exists(
            cleaned_data['username'])
        self._valdiate_password_match(
            cleaned_data['password'], cleaned_data['confirm_password'])
        return cleaned_data

    def _validate_user_with_supplied_email_exits(self, email):
        try:
            User.objects.get(email=email)
            self.add_error(
                "email", "User with this email already exist. Please sign up with another email or sign in with the existing account")
        except User.DoesNotExist:
            pass
        except Exception as e:
            raise(e)

    def _validate_user_with_supplied_username_exists(self, username):
        try:
            user = User.objects.get(username=username)
            self.add_error(
                "username", "User with this username exists. Please try out something else.")
        except User.DoesNotExist:
            pass
        except Exception as e:
            raise(e)

    def _valdiate_password_match(self, password, cfrm_password):
        if password != cfrm_password:
            self.add_error(
                "password", "The passwords you supplied didn't match. Try again.")


class LoginFormMixin:

    def _validate_user_exist(self, login_id: str):
        try:
            User.objects.get(email=login_id)
        except User.DoesNotExist:
            try:
                User.objects.get(username=login_id)
            except User.DoesNotExist:
                is_email = self._is_email(login_id)
                if is_email:
                    self.add_error(
                        'login_id', 'Account with the submitted email does not exist.')
                else:
                    self.add_error(
                        'login_id', 'Account with the submitted username does not exist.')
            except Exception as e:
                raise(e)
        except Exception as e:
            raise(e)

    def _is_email(self, login_id: str) -> bool:
        return '@' in login_id

    def _authenticate_user(self, login_id: str, password: str):
        is_email = self._is_email(login_id)
        user = None
        if is_email:
            user = authenticate(username=User.objects.get(
                email=login_id).username, password=password)
        else:
            user = authenticate(username=login_id, password=password)
        if user is None:
            try:
                user = User.objects.get(username=self.get_username(login_id))
            except User.DoesNotExist:
                # self.add_error('login_id', 'User does not exist')
                pass
            except Exception as e:
                raise(e)

            if user is not None:
                correct_password = user.check_password(password)
                if correct_password:
                    self.add_error(
                        'login_id', 'Your account has been disabled')
            self.add_error('password', 'Incorrect password')

    def get_username(self, login_id: str) -> str:
        if self._is_email(login_id):
            return User.objects.get(email=login_id).username
        return login_id
