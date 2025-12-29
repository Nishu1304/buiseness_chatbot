from django.db import models
from apps.clients.models import Client


class Lead(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("client", "phone")

    def __str__(self):
        return f"{self.name} ({self.phone})"
