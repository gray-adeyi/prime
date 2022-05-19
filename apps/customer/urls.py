from unicodedata import name
from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('login/', views.login_customer, name='login'),
    path('logout/', views.logout_customer, name='logout'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('book-job/', views.book_job, name='book-job'),
    path('create-new-booking/', views.create_new_booking, name='new-booking'),
    path('inc-exposure/<int:id>/', views.inc_exposure, name='inc'),
    path('dec-exposure/<int:id>/', views.dec_exposure, name='dec'),
    path('del-exposure/<int:id>/', views.del_exposure, name='del'),
    path('pending-jobs/', views.pending_jobs, name='pending-jobs'),
    path('show-pending-jobs/<int:id>/',
         views.show_pending_jobs, name='show-pending-jobs'),
    path('pay-methods/<int:id>/', views.pay_methods, name='pay-methods'),
    path('transfer-and-verify/<int:job_id>/',
         views.transfer_and_verify, name='transfer-and-verify'),
    path('confirm-discard/<int:job_id>/',
         views.confirm_discard, name='confirm-discard'),
    path('discard-booking/<int:job_id>/',
         views.discard_booking, name='discard-booking'),
    path('download-job/<int:job_id>/', views.download_job, name='download-job'),
]
