from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class RegistrationTest(TestCase):
    def test_registration_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'user@example.com',
        })
        self.assertEqual(response.status_code, 302)  # redirect after success
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'wrongpass',
            'email': 'user@example.com',
        })
        self.assertEqual(response.status_code, 200)  # form re-displayed
        self.assertFalse(User.objects.filter(username='newuser').exists())

class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'secret',
        })
        self.assertEqual(response.status_code, 302)  # redirect after login
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrong',
        })
        self.assertEqual(response.status_code, 200)  # form with error
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_logout(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)


class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.profile_url = reverse('profile')  # adjust to your URL name

    def test_profile_requires_login(self):
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.profile_url}")

    def test_profile_logged_in(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')  # check that username appears