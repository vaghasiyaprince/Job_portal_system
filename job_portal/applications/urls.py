from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('view-applicants/', views.view_applicants, name='view_applicants'),
    path('applicant/<int:app_id>/', views.applicant_detail, name='applicant_detail'),
    path('applications/success/', views.application_success, name='application_success'),
]