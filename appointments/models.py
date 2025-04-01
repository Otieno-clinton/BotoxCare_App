from django.contrib.auth.models import User
from django.db import models

from specialists.models import Specialist
from treatments.models import Treatment


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)  # Assuming a name, could be a ForeignKey if specialists are modeled
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Scheduled")

    def __str__(self):
        return f"{self.user.username} - {self.treatment.name} on {self.date}"
