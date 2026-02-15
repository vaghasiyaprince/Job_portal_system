from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/job-seeker/', views.job_seeker_register, name='job_seeker_register'),
    path('register/recruiter/', views.recruiter_register, name='recruiter_register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
