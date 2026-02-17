from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import JobSeeker, Recruiter
from django.contrib.auth.hashers import make_password, check_password


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
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # check job seeker
            user = JobSeeker.objects.filter(email=email).first()
            if user and check_password(password, user.password):
                request.session["user_type"] = "job_seeker"
                request.session["user_email"] = email
                return redirect("dashboard")

            # check recruiter
            recruiter = Recruiter.objects.filter(email=email).first()
            if recruiter and check_password(password, recruiter.password):
                request.session["user_type"] = "recruiter"
                request.session["user_email"] = email
                return redirect("dashboard")

            form.add_error(None, "Invalid email or password")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


# ================= LOGOUT =================
def logout_view(request):
    request.session.flush()
    return redirect("login")


# ================= DASHBOARD =================
def dashboard(request):
    user_type = request.session.get("user_type")
    user_email = request.session.get("user_email")

    if not user_type or not user_email:
        return redirect("login")

    if user_type == "job_seeker":
        user = JobSeeker.objects.filter(email=user_email).first()
        if not user:
            return redirect("login")
        return render(request, "jobseeker-dashboard.html", {"user": user})

    elif user_type == "recruiter":
        user = Recruiter.objects.filter(email=user_email).first()
        if not user:
            return redirect("login")
        return render(request, "recruiter-dashboard.html", {"user": user})

    return redirect("login")


# ================= HOME =================
def home(request):
    return render(request, "index.html")
