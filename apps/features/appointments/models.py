from django.db import models
from apps.clients.models import Client


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=255)

    service = models.CharField(max_length=255)
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=20)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} | {self.service} | {self.appointment_date} {self.appointment_time}"
