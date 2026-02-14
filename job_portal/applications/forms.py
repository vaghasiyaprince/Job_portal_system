from django import forms

class ApplicationForm(forms.Form):
    college = forms.CharField(max_length=150)
    branch = forms.CharField(max_length=100)
    result = forms.DecimalField(max_digits=5, decimal_places=2)
    resume = forms.FileField()
    experience = forms.CharField(widget=forms.Textarea)
    reason_to_join = forms.CharField(widget=forms.Textarea)
