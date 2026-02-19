from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import JobForm
from .models import Job
from accounts.models import Recruiter


def post_job(request):
    if request.session.get('user_type') != 'recruiter':
        return redirect('login ')

    if request.method == 'POST':
        recruiter = Recruiter.objects.filter(
            email=request.session.get('user_email')
        ).first()

        if not recruiter:
            return redirect('login')

        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')
        skills = request.POST.get('skills_required')
        description = request.POST.get('job_description')

        if not job_title or not company_name or not skills or not description:
            return render(request, 'post-job.html', {
                'error': 'All fields are required'
            })

        skills = ", ".join([s.strip() for s in skills.split(",")])

        Job.objects.create(
            recruiter=recruiter,
            job_title=job_title,
            skills_required=skills,
            job_description=description,
            company_name=company_name
        )

        return redirect('dashboard')

    return render(request, 'post-job.html')

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job-list.html', {'jobs': jobs})


def job_detail(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return HttpResponse("Job not found")

    return render(request, 'job-details.html', {'job': job})

