from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('post/', views.post_job, name='post_job'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('post-success/', views.job_post_success, name='job_post_success'),
]
