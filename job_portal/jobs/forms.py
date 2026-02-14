from django import forms

class JobForm(forms.Form):
    job_title = forms.CharField(max_length = 150)
    job_description = forms.CharField(widget=forms.Textarea)
    skills_required = forms.CharField(
        widget=forms.Textarea,
        help_text="List skills separated by commas")
    company_name = forms.CharField(max_length = 150)