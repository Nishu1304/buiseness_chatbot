from django.db import models
from apps.clients.models import Client
from django.utils import timezone
from datetime import timedelta

class ConversationSession(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user_phone = models.CharField(max_length=20)

    state = models.CharField(max_length=50, null=True, blank=True)
    context = models.JSONField(default=dict)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("client", "user_phone")

    def is_expired(self, ttl_minutes=15):
        return timezone.now() - self.updated_at > timedelta(minutes=ttl_minutes)
