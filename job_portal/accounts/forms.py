from django import forms

class JobSeekerRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    contact = forms.CharField(max_length=15)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class RecruiterRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    contact = forms.CharField(max_length=15)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    company_name = forms.CharField(max_length=150)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)