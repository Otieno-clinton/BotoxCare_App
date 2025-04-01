from django.db import models
from django.contrib.auth.models import User












from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('specialist', 'Specialist'),
        ('admin', 'Clinic Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')  # ✅ Add this field

    def __str__(self):
        return f"{self.user.username} - {self.role}"




