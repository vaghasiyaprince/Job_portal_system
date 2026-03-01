# from django.shortcuts import redirect, render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ApplicationForm
from .models import Application
from accounts.models import JobSeeker,Recruiter
from jobs.models import Job
from django.contrib.auth.decorators import login_required
 

def apply_job(request, job_id):

    if not request.session.get("user_type"):
        request.session["required_role"] = "job_seeker"
        request.session["next_url"] = request.path
        return redirect("login")

    if request.session.get("user_type") != "job_seeker":
        return HttpResponse("You are not a Job Seeker")

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return HttpResponse("Job not found")

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            job_seeker = JobSeeker.objects.get(email=request.session['user_email'])
            
            if Application.objects.filter(job=job, job_seeker=job_seeker).exists():
                return render(request, 'application-success.html',
                              {'message': 'You have already applied for this job.'} )
                
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

            return redirect('application-success.html')

    else:
        form = ApplicationForm()

    return render(request, 'application-form.html', {'form': form, 'job': job})


def view_applicants(request):
    if not request.session.get("user_type"):
        request.session["required_role"] = "recruiter"
        request.session["next_url"] = request.path
        return redirect("login")

    if request.session.get("user_type") != "recruiter":
        return HttpResponse("You are not a Recruiter")
    
    recruiter = Recruiter.objects.filter(
        email=request.session['user_email']
    ).first()

    applications = Application.objects.filter(
        job__recruiter=recruiter
    )

    return render(request, 'applicants-list.html', {
        'applications': applications
    })

# @login_required
# def submit_application(request, job_id):
#     job = get_object_or_404(Job, id=job_id)

#     if request.method == 'POST':
#         form = ApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             application = form.save(commit=False)
#             application.job = job
#             application.applicant = request.user
#             application.save()
#             # Optional: success message
#             # messages.success(request, "Application submitted successfully!")
#             return redirect('job_list')   # or wherever you want to go after apply

#     else:
#         form = ApplicationForm()

#     return render(request, 'application-form.html', {
#         'form': form,
#         'job': job,
#         'job_id': job_id,
#     })

def applicant_detail(request, app_id):
    if request.session.get('user_type') != 'recruiter':
        request.session["required_role"] = "recruiter"
        request.session["next_url"] = request.path
        return redirect('login')

    application = Application.objects.filter(id=app_id).first()

    if not application:
        return redirect('view_applicants')

    return render(request, 'applicant-details.html', {
        'application': application
    })