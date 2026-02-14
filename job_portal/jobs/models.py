from django.db import models
from accounts.models import Recruiter


class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=150)
    skills_required = models.TextField()
    job_description = models.TextField()
    company_name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title
