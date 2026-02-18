from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('post/', views.post_job, name='post_job'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    # urls.py
    path('', views.landing_page, name='home'), # by hitesh
]
