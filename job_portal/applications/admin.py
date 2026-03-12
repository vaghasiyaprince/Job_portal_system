from django.contrib import admin
from .models import Application

# Register your models here.
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_seeker', 'job', 'college', 'branch', 'result', 'applied_at')
    list_filter = ('applied_at', 'job', 'college')
    search_fields = ('job_seeker__name', 'job__job_title', 'college', 'branch')
    readonly_fields = ('applied_at',)