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
        role = request.POST.get("role")
        company = request.POST.get("company_name")

        if not name or not email or not password or not role:
            return render(request, "register.html", {"error": "All fields are required"})

        # prevent duplicate email
        if JobSeeker.objects.filter(email=email).exists() or Recruiter.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already registered"})

        if role == "job_seeker":
            JobSeeker.objects.create(
                name=name,
                email=email,
                password=make_password(password)
            )

        elif role == "recruiter":
            if not company:
                return render(request, "register.html", {"error": "Company name required"})

            Recruiter.objects.create(
                name=name,
                email=email,
                password=make_password(password),
                company_name=company
            )

        return redirect("login")

    return render(request, "register.html")

# ================= LOGIN =================

def login_view(request):

    required_role = request.session.get("required_role")
    next_url = request.session.get("next_url")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # 🔵 Job Seeker Login
        if required_role == "job_seeker":
            user = JobSeeker.objects.filter(email=email).first()
            if user and check_password(password, user.password):
                # if required_role == "recruiter":
                #     return render(request, "login.html", {
                #         "form": form,
                #         "error": "You are not a Recruiter"
                #     })
                request.session["user_type"] = "job_seeker"
                request.session["user_email"] = email

                request.session.pop("required_role", None)

                if next_url:
                    request.session.pop("next_url", None)
                    return redirect(next_url)

                return redirect("job_list")
            else:
                return render(request, "login.html", {
                    "form": form,
                    "error": "Invalid email or password"
                })

            # 🔵 Recruiter Login
        else:
            recruiter = Recruiter.objects.filter(email=email).first()
            if recruiter and check_password(password, recruiter.password):

                # if required_role == "job_seeker":
                #     return render(request, "login.html", {
                #         "form": form,
                #         "error": "You are not a Job Seeker"
                #     })

                request.session["user_type"] = "recruiter"
                request.session["user_email"] = email

                request.session.pop("required_role", None)

                if next_url:
                    request.session.pop("next_url", None)
                    return redirect(next_url)

                return redirect("recruiter_dashboard")

            return render(request, "login.html", {
                "form": form,
                "error": "Invalid email or password"
            })

    else:
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
    request.session["required_role"] = "recruiter"
    request.session["next_url"] = request.path
    if request.GET.get("preview"):
        return render(request, "recruiter-dashboard.html")

    # Not logged in
    # if not request.session.get("user_type"):
        
        # return redirect("login")

    # Wrong role
    if request.session.get("user_type") != "recruiter":
        return redirect("job_list")

    return render(request, "recruiter-dashboard.html")

# ================= HOME =================
def home(request):
    return render(request, "index.html")
