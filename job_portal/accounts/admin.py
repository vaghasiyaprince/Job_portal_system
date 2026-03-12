from django.contrib import admin
from .models import JobSeeker, Recruiter

# Register your models here.
@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')

@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'company_name')
    search_fields = ('name', 'email', 'company_name')