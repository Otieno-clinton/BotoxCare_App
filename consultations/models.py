from django.contrib.auth.models import User
from django.db import models

from specialists.models import Specialist


# ---------------- Consultations ----------------
class Consultation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    room_name = models.CharField(max_length=255, unique=True, blank=True, null=True)  # ✅ Unique room name

    def save(self, *args, **kwargs):
        if not self.room_name:
            self.room_name = f"Consultation_{self.pk}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Consultation with {self.specialist.full_name} on {self.date}"
