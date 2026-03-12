from django.contrib import admin
from .models import Job

# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title', 'company_name', 'recruiter', 'created_at')
    list_filter = ('created_at', 'company_name')
    search_fields = ('job_title', 'company_name', 'skills_required')
    readonly_fields = ('created_at',)