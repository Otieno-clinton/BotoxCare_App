from django.contrib.auth.models import User
from django.db import models

class Specialist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="specialist_profile")
    is_active = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255, choices=[
        ("Dermatologist", "Dermatologist"),
        ("Plastic Surgeon", "Plastic Surgeon"),
        ("Cosmetic Specialist", "Cosmetic Specialist"),
        ("Licensed Professional", "Licensed Professional"),
    ])
    credentials = models.TextField(help_text="List of professional qualifications and licenses.")
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True, null=True, help_text="Short professional biography.")
    available_days = models.CharField(max_length=100, help_text="E.g., Monday-Friday")
    working_hours = models.CharField(max_length=100, help_text="E.g., 9:00 AM - 5:00 PM")
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    accepts_virtual_consultations = models.BooleanField(default=True)
    accepts_in_person_consultations = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False, help_text="Admin approval for specialists.")

    def __str__(self):
        return f"{self.full_name} ({self.specialty})"

# ✅ Add this property to the User model dynamically
User.add_to_class("is_specialist", property(lambda u: hasattr(u, "specialist_profile")))
