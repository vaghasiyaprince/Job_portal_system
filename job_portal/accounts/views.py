from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from .models import JobSeeker, Recruiter
from django.contrib.auth.hashers import make_password, check_password
from jobs.models import Job
from applications.models import Application
from django.contrib.auth import get_user_model
User = get_user_model()
import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from . import views


# ================= REGISTER =================
# def register(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email").lower()
#         password = request.POST.get("password")
#         contact = request.POST.get("contact")
#         role = request.POST.get("role")
#         company = request.POST.get("company_name")

#         if not name or not email or not password or not role:
#             return render(request, "register.html", {"error": "All fields are required"})

#         if JobSeeker.objects.filter(email=email).exists() or Recruiter.objects.filter(email=email).exists():
#             return render(request, "register.html", {"error": "Email already registered"})

#         if role == "job_seeker":
#             JobSeeker.objects.create(
#                 name=name,
#                 email=email,
#                 password=make_password(password),
#                 contact=contact
#             )

#         elif role == "recruiter":
#             if not company:
#                 return render(request, "register.html", {"error": "Company name required"})

#             Recruiter.objects.create(
#                 name=name,
#                 email=email,
#                 password=make_password(password),
#                 contact=contact,
#                 company_name=company
#             )

#         return redirect("home")

#     return render(request, "register.html")



# ================= REGISTER =================
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")   # ✅ ADDED
        contact = request.POST.get("contact")
        role = request.POST.get("role")
        company = request.POST.get("company_name")

        # ✅ CHECK REQUIRED FIELDS
        if not name or not email or not password or not confirm_password or not role:
            return render(request, "register.html", {"error": "All fields are required"})

        # ✅ CHECK PASSWORD MATCH
        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

        # ✅ CHECK EMAIL EXISTS
        if JobSeeker.objects.filter(email=email).exists() or Recruiter.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already registered"})

        # ✅ CREATE USER
        if role == "job_seeker":
            JobSeeker.objects.create(
                name=name,
                email=email,
                password=make_password(password),   # ✅ already correct
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


# ================= Reset Password =================
# def reset_password(request, user_id):
#     user = User.objects.get(id=user_id)

#     if request.method == "POST":
#         password = request.POST.get("password")
#         confirm_password = request.POST.get("confirm_password")

#         if password != confirm_password:
#             return render(request, 'reset-password.html', {'error': 'Passwords do not match'})

#         user.password = password
#         user.save()
#         return redirect('login')

#     return render(request, 'reset-password.html')



# ================= Reset Password =================
# def reset_password(request, user_id):
#     user = User.objects.get(id=user_id)

#     if request.method == "POST":
#         password = request.POST.get("password")
#         confirm_password = request.POST.get("confirm_password")

#         if password != confirm_password:
#             return render(request, 'reset-password.html', {'error': 'Passwords do not match'})

#         # ✅ SECURE PASSWORD SAVE
#         user.password = make_password(password)
#         user.save()

#         return redirect('login')

#     return render(request, 'reset-password.html')


def reset_password_otp(request):
    email = request.GET.get("email")

    user = JobSeeker.objects.filter(email=email).first() or Recruiter.objects.filter(email=email).first()

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "reset-password.html", {"error": "Passwords do not match"})

        user.password = make_password(password)

        # ✅ clear OTP
        user.otp = None
        user.save()

        return redirect("login")

    return render(request, "reset-password.html")

   
# ================= Forget Password =================

# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')

#         try:-
#             user = User.objects.get(email=email)
#             # do your logic here
#         except User.DoesNotExist:
#             print("User not found")

#     return render(request, 'forgot-password.html')



def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        user = JobSeeker.objects.filter(email=email).first() or Recruiter.objects.filter(email=email).first()

        if not user:
            return render(request, "forgot-password.html", {"error": "Email not found"})

        # ✅ Generate OTP
        otp = str(random.randint(100000, 999999))

        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        # ✅ Send Email
        send_mail(
    "OTP Verification",
    f"Your OTP is: {otp}",
    "your_email@gmail.com",
    [email],
    fail_silently=False,
)
        return redirect("verify_otp", email=email)

    return render(request, "forgot-password.html")


def verify_otp(request):
    email = request.GET.get("email")

    user = JobSeeker.objects.filter(email=email).first() or Recruiter.objects.filter(email=email).first()

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        # ⏳ OTP expiry (5 min)
        if timezone.now() > user.otp_created_at + timedelta(minutes=5):
            return render(request, "verify-otp.html", {"error": "OTP expired", "email": email})

        if entered_otp != user.otp:
            return render(request, "verify-otp.html", {"error": "Invalid OTP", "email": email})

        return redirect("reset_password_otp", email=email)

    return render(request, "verify-otp.html", {"email": email})




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