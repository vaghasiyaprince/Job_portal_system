from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import ApplicationForm
from .models import Application
from accounts.models import JobSeeker
from jobs.models import Job


def apply_job(request, job_id):
    if 'user_type' not in request.session or request.session['user_type'] != 'job_seeker':
        return redirect('login')

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return HttpResponse("Job not found")

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            job_seeker = JobSeeker.objects.get(email=request.session['user_email'])

            Application.objects.create(
                job=job,
                job_seeker=job_seeker,
                college=form.cleaned_data['college'],
                branch=form.cleaned_data['branch'],
                result=form.cleaned_data['result'],
                resume=form.cleaned_data['resume'],
                experience=form.cleaned_data['experience'],
                reason_to_join=form.cleaned_data['reason_to_join']
            )

            return redirect('dashboard')

    else:
        form = ApplicationForm()

    return HttpResponse("Application form backend working")


def view_applicants(request):
    if 'user_type' not in request.session or request.session['user_type'] != 'recruiter':
        return redirect('login')

    applications = Application.objects.all()

    return HttpResponse("Applicants list backend working")
