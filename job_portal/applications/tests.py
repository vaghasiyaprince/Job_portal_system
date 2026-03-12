from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Application
from jobs.models import Job
from accounts.models import JobSeeker, Recruiter

# Create your tests here.
class ApplicationModelTest(TestCase):
    def setUp(self):
        # Create a recruiter and a job
        self.recruiter = Recruiter.objects.create(
            name="Test Recruiter",
            email="recruiter@test.com",
            password="testpass",
            company_name="Test Company"
        )
        self.job = Job.objects.create(
            recruiter=self.recruiter,
            job_title="Software Engineer",
            skills_required="Python, Django",
            job_description="Build web apps",
            company_name="Test Company"
        )
        self.job_seeker = JobSeeker.objects.create(
            name="John Doe",
            email="john@test.com",
            password="testpass"
        )

    def test_application_creation(self):
        # Create a simple in-memory file for resume
        resume_file = SimpleUploadedFile(
            "resume.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        application = Application.objects.create(
            job=self.job,
            job_seeker=self.job_seeker,
            college="Test University",
            branch="Computer Science",
            result=8.5,
            resume=resume_file,
            experience="2 years internship",
            reason_to_join="I love coding"
        )
        self.assertEqual(application.job.job_title, "Software Engineer")
        self.assertEqual(application.job_seeker.name, "John Doe")
        self.assertEqual(application.college, "Test University")
        self.assertIsNotNone(application.applied_at)
        self.assertEqual(str(application), "John Doe - Software Engineer")

    def test_unique_application_constraint(self):
        # Create first application
        resume_file = SimpleUploadedFile("resume.pdf", b"content", content_type="application/pdf")
        Application.objects.create(
            job=self.job,
            job_seeker=self.job_seeker,
            college="Test University",
            branch="CS",
            result=8.5,
            resume=resume_file,
            experience="",
            reason_to_join=""
        )
        # Try to create duplicate
        with self.assertRaises(Exception):  # Django should raise IntegrityError
            Application.objects.create(
                job=self.job,
                job_seeker=self.job_seeker,
                college="Another",
                branch="ECE",
                result=7.0,
                resume=resume_file,
                experience="",
                reason_to_join=""
            )


class ApplicationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.recruiter = Recruiter.objects.create(
            name="Recruiter",
            email="rec@test.com",
            password="pass",
            company_name="Rec Inc"
        )
        self.job_seeker = JobSeeker.objects.create(
            name="Seeker",
            email="seek@test.com",
            password="pass"
        )
        self.job = Job.objects.create(
            recruiter=self.recruiter,
            job_title="Developer",
            skills_required="Python",
            job_description="Coding",
            company_name="Rec Inc"
        )

    def test_apply_job_view_requires_login(self):
        response = self.client.get(reverse('apply_job', args=[self.job.id]))
        # Should redirect to login because user not logged in (session empty)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_apply_job_view_with_job_seeker_session(self):
        # Simulate logged-in job seeker
        session = self.client.session
        session['user_type'] = 'job_seeker'
        session['user_email'] = self.job_seeker.email
        session.save()

        response = self.client.get(reverse('apply_job', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application-form.html')

    def test_apply_job_post_success(self):
        session = self.client.session
        session['user_type'] = 'job_seeker'
        session['user_email'] = self.job_seeker.email
        session.save()

        resume_file = SimpleUploadedFile("resume.pdf", b"content", content_type="application/pdf")
        post_data = {
            'college': 'University',
            'branch': 'CS',
            'result': 8.5,
            'resume': resume_file,
            'experience': 'Some experience',
            'reason_to_join': 'Good company'
        }
        response = self.client.post(reverse('apply_job', args=[self.job.id]), post_data, format='multipart')
        # After successful post, redirects to dashboard (or wherever)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))  # adjust if different

        # Check application was created
        self.assertTrue(Application.objects.filter(job=self.job, job_seeker=self.job_seeker).exists())