from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/jobseeker/', views.jobseeker_profile, name='jobseeker_profile'),
    path('profile/recruiter/', views.recruiter_profile, name='recruiter_profile'),        
    path('recruiter-dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
]
