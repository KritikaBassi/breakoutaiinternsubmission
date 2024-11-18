from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
    path('create_prompt/', views.create_prompt, name='create_prompt'),
    path('schedule_emails/', views.schedule_emails, name='schedule_emails'),
    path('email_status/', views.email_status, name='email_status'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
