from unicodedata import name
from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('login/', views.login_customer, name='login'),
    path('logout/', views.logout_customer, name='logout'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
]
