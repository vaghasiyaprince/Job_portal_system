from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    # path('forgot-password/', views.forgot_password, name='forgot_password'),
    # path('reset-password-otp/', views.reset_password_otp, name='reset_password_otp')
    path('logout/', views.logout_view, name='logout'),
    path('jobseeker-dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    path('recruiter-dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password-otp/', views.reset_password_otp, name='reset_password_otp'),
]
