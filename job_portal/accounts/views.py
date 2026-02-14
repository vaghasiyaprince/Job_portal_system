from django.shortcuts import render, redirect
from .forms import JobSeekerRegistrationForm, RecruiterRegistrationForm, LoginForm
from .models import JobSeeker, Recruiter
from django.contrib.auth.hashers import make_password, check_password


def job_seeker_register(request):
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST)
        if form.is_valid():
            JobSeeker.objects.create(
                name=form.cleaned_data['name'],
                contact=form.cleaned_data['contact'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password'])
            )
            return redirect('login')
    else:
        form = JobSeekerRegistrationForm()
        
    return render(request, 'accounts/job_seeker_register.html', {'form': form})


def recruiter_register(request):
    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            Recruiter.objects.create(
                name=form.cleaned_data['name'],
                contact=form.cleaned_data['contact'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password']),
                company_name=form.cleaned_data['company_name']
            )
            return redirect('login')
    else:
        form = RecruiterRegistrationForm()

    return render(request, 'accounts/recruiter_register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = JobSeeker.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_type'] = 'job_seeker'
                    request.session['user_email'] = email
                    return redirect('dashboard')
            except JobSeeker.DoesNotExist:
                pass

            try:
                recruiter = Recruiter.objects.get(email=email)
                if check_password(password, recruiter.password):
                    request.session['user_type'] = 'recruiter'
                    request.session['user_email'] = email
                    return redirect('dashboard')  
            except Recruiter.DoesNotExist:
                pass

            form.add_error(None, "Invalid email or password")

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})



def logout_view(request):
    request.session.flush()
    return redirect('login')

def dashboard(request):
    user_type = request.session.get('user_type')
    user_email = request.session.get('user_email')

    if user_type == 'job_seeker':
        user = JobSeeker.objects.get(email=user_email)
        return render(request, 'accounts/job_seeker_dashboard.html', {'user': user})
    elif user_type == 'recruiter':
        user = Recruiter.objects.get(email=user_email)
        return render(request, 'accounts/recruiter_dashboard.html', {'user': user})
    else:
        return redirect('login')
