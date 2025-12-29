from django.db import models
from apps.clients.models import Client


class Feedback(models.Model):
    feedback_id = models.BigAutoField(primary_key=True)

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="feedbacks",
        db_index=True,
    )

    phone = models.CharField(max_length=20)
    rating = models.IntegerField()  # 1–5
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rating}⭐ ({self.client.name})"
