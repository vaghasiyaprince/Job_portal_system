from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from .models import JobSeeker, Recruiter
from django.contrib.auth.hashers import make_password, check_password
from jobs.models import Job
from applications.models import Application

# ================= REGISTER =================
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        contact = request.POST.get("contact")
        role = request.POST.get("role")
        company = request.POST.get("company_name")

        if not name or not email or not password or not role:
            return render(request, "register.html", {"error": "All fields are required"})

        if JobSeeker.objects.filter(email=email).exists() or Recruiter.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already registered"})

        if role == "job_seeker":
            JobSeeker.objects.create(
                name=name,
                email=email,
                password=make_password(password),
                contact=contact
            )

        elif role == "recruiter":
            if not company:
                return render(request, "register.html", {"error": "Company name required"})

            Recruiter.objects.create(
                name=name,
                email=email,
                password=make_password(password),
                contact=contact,
                company_name=company
            )

        return redirect("home")

    return render(request, "register.html")

# ================= LOGIN =================
def login_view(request):
    # Get session variables if they exist
    required_role = request.session.get("required_role")
    next_url = request.session.get("next_url")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Check if user is a Job Seeker
            job_seeker = JobSeeker.objects.filter(email=email).first()
            if job_seeker and check_password(password, job_seeker.password):
                # If a specific role was required, verify it matches
                if required_role and required_role != "job_seeker":
                    return render(request, "login.html", {
                        "form": form,
                        "error": "This page requires a Recruiter account. Please login as a Recruiter."
                    })

                # Set session
                request.session["user_type"] = "job_seeker"
                request.session["user_email"] = email
                request.session["user_name"] = job_seeker.name

                # Clear temporary session data
                request.session.pop("required_role", None)
                request.session.pop("next_url", None)

                # Redirect to next_url if exists, otherwise to default
                if next_url:
                    return redirect(next_url)
                return redirect("job_list")

            # Check if user is a Recruiter
            recruiter = Recruiter.objects.filter(email=email).first()
            if recruiter and check_password(password, recruiter.password):
                # If a specific role was required, verify it matches
                if required_role and required_role != "recruiter":
                    return render(request, "login.html", {
                        "form": form,
                        "error": "This page requires a Recruiter account. Please login as a job seeker."
                    })

                # Set session
                request.session["user_type"] = "recruiter"
                request.session["user_email"] = email
                request.session["user_name"] = recruiter.name

                # Clear temporary session data
                request.session.pop("required_role", None)
                request.session.pop("next_url", None)

                # Redirect to next_url if exists, otherwise to default
                if next_url:
                    return redirect(next_url)
                return redirect("recruiter_dashboard")

            # If no user found with these credentials
            return render(request, "login.html", {
                "form": form,
                "error": "Invalid email or password"
            })

        # If form is invalid
        return render(request, "login.html", {"form": form})

    # GET request - display empty form
    form = LoginForm()
    return render(request, "login.html", {"form": form})

# ================= LOGOUT =================
def logout_view(request):
    request.session.flush()
    return redirect("home")

# ================= DASHBOARD =================
def jobseeker_dashboard(request):
    if request.session.get('user_type') != 'job_seeker':
        return redirect('login')

    jobs = Job.objects.all()
    return render(request, 'job-list.html', {'jobs': jobs})

def recruiter_dashboard(request):
    # Preview mode (from home)
    if request.GET.get("preview"):
        request.session["required_role"] = "recruiter"
        request.session["next_url"] = request.path
        return render(request, "recruiter-dashboard.html")

    # Check if user is logged in as recruiter
    if request.session.get("user_type") != "recruiter":
        return redirect("login")

    return render(request, "recruiter-dashboard.html")

# ================= HOME =================
def home(request):
    return render(request, "index.html")