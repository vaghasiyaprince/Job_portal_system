from django.test import TestCase
from django.urls import reverse
from .models import JobSeeker, Recruiter
from django.contrib.auth.hashers import make_password

class RegistrationTest(TestCase):
    def test_registration_success(self):
        response = self.client.post(reverse('register'), {
            'name': 'newuser',
            'email': 'user@example.com',
            'password': 'testpass123',
            'contact': '1234567890',
            'role': 'job_seeker',
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(JobSeeker.objects.filter(email='user@example.com').exists())

    def test_registration_password_mismatch(self):
        pass

class LoginTest(TestCase):
    def setUp(self):
        self.job_seeker = JobSeeker.objects.create(
            name='testuser',
            email='test@example.com',
            password=make_password('testpass123'),
            contact='1234567890'
        )

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue('user_type' in self.client.session)

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'wrong',
        })
        self.assertEqual(response.status_code, 200) 
        self.assertFalse('user_type' in self.client.session)

    def test_logout(self):
        session = self.client.session
        session['user_type'] = 'job_seeker'
        session['user_email'] = 'test@example.com'
        session.save()
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('user_type' in self.client.session)


