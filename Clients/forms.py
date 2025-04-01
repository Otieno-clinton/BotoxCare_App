from django import forms
from django.contrib.auth.models import User

from Clients.models import Profile


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"name": "password1"}), label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"name": "password2"}), label="Confirm Password"
    )
    medical_history = forms.CharField(
        widget=forms.Textarea, required=False, label="Medical History (Optional)"
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "email", "date_of_birth", "role"]