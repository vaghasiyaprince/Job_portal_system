from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import JobForm
from .models import Job
from accounts.models import Recruiter
from . import views

def post_job(request):
    if not request.session.get("user_type"):
        request.session["required_role"] = "recruiter"
        request.session["next_url"] = request.path
        return redirect("login")

    if request.session.get("user_type") != "recruiter":
        return redirect("login")

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
        location = request.POST.get('location')

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
            location=location 
            # company_name=company_name
        )

        return redirect('job_post_success')

    return render(request, 'post-job.html')

def job_list(request):
    request.session["required_role"] = "job_seeker"
    request.session["next_url"] = request.path

    jobs = Job.objects.all()
    query = request.GET.get('q')

    if query:
        jobs = jobs.filter(
            Q(job_title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(skills_required__icontains=query)
        )

    return render(request, 'job-list.html', {
        'jobs': jobs,
        'query': query
    })

def job_detail(request, job_id):
    job = Job.objects.filter(id=job_id).first()
    if not job:
        return redirect('job_list')

    if not request.session.get("user_type"):
        request.session["required_role"] = "job_seeker"
        request.session["next_url"] = request.path
        return redirect("login")

    if request.session.get("user_type") != "job_seeker":
        return redirect("login")

    return render(request, 'job-details.html', {'job': job})

def job_post_success(request):
    return render(request, 'post-job-success.html')