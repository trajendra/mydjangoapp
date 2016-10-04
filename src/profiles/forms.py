from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "slug",
            "image",
            "profile",
            "skills",
            "learn_interests",
            "email",
        ]

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
