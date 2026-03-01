from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    # path('apply/<int:job_id>/submit/', views.submit_application, name='submit_application'),
    path('view-applicants/', views.view_applicants, name='view_applicants'),
    path('applicant/<int:app_id>/', views.applicant_detail, name='applicant_detail'),
]