from django import forms
from typing import Optional, Mapping, Any
from django.contrib.auth.models import User
from apps.core.forms import LoginFormMixin
from . import models


class LoginForm(LoginFormMixin, forms.Form):
    login_id = forms.CharField(max_length=50, label="EMAIL/USERNAME")
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean(self) -> Optional[Mapping[str, Any]]:
        cleaned_data = super().clean()
        # Had to create a copy of the cleaned data as python pops fields from the cleaned data dict when it fails a validation
        persistent_data = cleaned_data.copy()
        self._validate_user_exist(persistent_data['login_id'])
        self._authenticate_user(
            persistent_data['login_id'], persistent_data['password'])
        self._validate_user_is_customer(persistent_data['login_id'])
        return cleaned_data

    def _validate_user_is_customer(self, login_id: str):
        is_email = self._is_email(login_id)
        user = None
        if is_email:
            try:
                user = User.objects.get(email=login_id)
            except User.DoesNotExist:
                self.add_error('login_id', 'User does not exist')
            except Exception as e:
                raise(e)
        else:
            try:
                user = User.objects.get(username=login_id)
            except User.DoesNotExist:
                self.add_error('login_id', 'User does not exist')
            except Exception as e:
                raise(e)
        try:
            models.Customer.objects.get(user=user)
        except models.Customer.DoesNotExist:
            self.add_error('login_id', 'Customer account does not exist')
        except Exception as e:
            raise(e)
