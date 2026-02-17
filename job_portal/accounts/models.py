from django.db import models

class JobSeeker(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recruiter(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    company_name = models.CharField(max_length=150)

    def __str__(self):
        return self.company_name
