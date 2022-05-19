from django.urls import path
from . import views

app_name = 'editor'

urlpatterns = [
    path('login/', views.login_editor, name='login'),
    path("dashboard/", views.Dashboard.as_view(), name="dashboard"),
    path("logout/", views.logout_editor, name="logout"),
]
