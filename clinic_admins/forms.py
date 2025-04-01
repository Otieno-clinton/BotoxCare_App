from django import forms
from django.contrib.auth.models import User
from .models import ClinicAdmin

class ClinicAdminRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    clinic_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=20, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"]
        )
        clinic_admin = ClinicAdmin.objects.create(
            user=user,
            clinic_name=self.cleaned_data["clinic_name"],
            phone_number=self.cleaned_data["phone_number"],
            address=self.cleaned_data["address"],
            is_active=False  # Require approval before activation
        )
        return user
