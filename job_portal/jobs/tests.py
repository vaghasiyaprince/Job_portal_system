from django.test import TestCase, Client
from django.urls import reverse
from .models import Job
from accounts.models import Recruiter

# Create your tests here.
class JobModelTest(TestCase):
    def setUp(self):
        self.recruiter = Recruiter.objects.create(
            name="Test Recruiter",
            email="rec@test.com",
            password="pass",
            company_name="Tech Corp"
        )

    def test_job_creation(self):
        job = Job.objects.create(
            recruiter=self.recruiter,
            job_title="Backend Developer",
            skills_required="Python, SQL",
            job_description="Build APIs",
            company_name="Tech Corp"
        )
        self.assertEqual(job.job_title, "Backend Developer")
        self.assertEqual(job.skills_required, "Python, SQL")
        self.assertIsNotNone(job.created_at)
        self.assertEqual(str(job), "Backend Developer")

    def test_job_ordering(self):
        job1 = Job.objects.create(
            recruiter=self.recruiter,
            job_title="Job A",
            skills_required="",
            job_description="",
            company_name="Tech Corp"
        )
        job2 = Job.objects.create(
            recruiter=self.recruiter,
            job_title="Job B",
            skills_required="",
            job_description="",
            company_name="Tech Corp"
        )
        # By default, ordering should be by created_at descending? Not set in model.
        # But we can test that both exist.
        self.assertEqual(Job.objects.count(), 2)


class JobViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.recruiter = Recruiter.objects.create(
            name="Recruiter",
            email="rec@test.com",
            password="pass",
            company_name="Rec Inc"
        )
        self.job = Job.objects.create(
            recruiter=self.recruiter,
            job_title="Developer",
            skills_required="Python",
            job_description="Coding",
            company_name="Rec Inc"
        )

    def test_job_list_view(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job-list.html')
        self.assertContains(response, "Developer")

    def test_job_detail_view(self):
        response = self.client.get(reverse('job_detail', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job-details.html')
        self.assertContains(response, "Developer")

    def test_post_job_view_requires_recruiter(self):
        # Not logged in
        response = self.client.get(reverse('post_job'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_post_job_view_with_recruiter_session(self):
        session = self.client.session
        session['user_type'] = 'recruiter'
        session['user_email'] = self.recruiter.email
        session.save()

        response = self.client.get(reverse('post_job'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post-job.html')

    def test_post_job_creates_job(self):
        session = self.client.session
        session['user_type'] = 'recruiter'
        session['user_email'] = self.recruiter.email
        session.save()

        post_data = {
            'job_title': 'New Job',
            'company_name': 'New Co',
            'skills_required': 'Django, React',
            'job_description': 'Full stack'
        }
        response = self.client.post(reverse('post_job'), post_data)
        # After successful post, redirects to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

        # Check job was created
        self.assertTrue(Job.objects.filter(job_title='New Job', company_name='New Co').exists())