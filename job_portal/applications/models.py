from django.db import models
from accounts.models import JobSeeker
from jobs.models import Job
import uuid
import os


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)

    college = models.CharField(max_length=150)
    branch = models.CharField(max_length=150)
    result = models.DecimalField(max_digits=5, decimal_places=2)
    resume = models.FileField(upload_to='resumes/')
    experience = models.TextField()
    reason_to_join = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.job_seeker.name} - {self.job.job_title}"



def upload_resume(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('resumes/', new_filename)