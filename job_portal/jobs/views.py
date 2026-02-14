from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import JobForm
from .models import Job
from accounts.models import Recruiter


def post_job(request):
    if 'user_type' not in request.session or request.session['user_type'] != 'recruiter':
        return redirect('login')

    if request.method == 'POST':
        form = JobForm(request.POST)

        if form.is_valid():
            recruiter = Recruiter.objects.filter(
                email=request.session.get('user_email')
            ).first()

            if not recruiter:
                return redirect('login')

            skills = form.cleaned_data['skills_required']
            skills = ", ".join([s.strip() for s in skills.split(",")])

            Job.objects.create(
                recruiter=recruiter,
                job_title=form.cleaned_data['job_title'],
                skills_required=skills,
                job_description=form.cleaned_data['job_description'],
                company_name=form.cleaned_data['company_name']
            )

            return redirect('dashboard')

    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return HttpResponse("Job not found")

    return render(request, 'jobs/job_detail.html', {'job': job})
