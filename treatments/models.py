from django.contrib.auth.models import User
from django.db import models

class Treatment(models.Model):
    specialist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="treatments", null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(help_text="Duration in HH:MM:SS format")
    risks = models.TextField(blank=True, null=True)
    precautions = models.TextField(blank=True, null=True)
    aftercare = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
