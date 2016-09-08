from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "image",
            "profile",
            "skills",
        ]
