from unicodedata import name
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('about/', views.About.as_view(), name='about'),
    path('sign-up/', views.Signup.as_view(), name='signup'),
]
