from django.db import models
from apps.clients.models import Client


class ScheduledMessage(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("SENT", "Sent"),
        ("FAILED", "Failed"),
    )

    TYPE_CHOICES = (
        ("FEEDBACK", "Feedback"),
        ("SURVEY", "Survey"),
        ("OFFER", "Offer"),
        ("REMINDER", "Reminder"),
    )

    scheduled_message_id = models.BigAutoField(primary_key=True)

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="scheduled_messages",
        db_index=True,
    )

    phone = models.CharField(max_length=20)

    message_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message_text = models.TextField()

    scheduled_at = models.DateTimeField(db_index=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING",
        db_index=True,
    )

    error = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["scheduled_at"]

    def __str__(self):
        return f"{self.message_type} → {self.phone} @ {self.scheduled_at}"
