from django.db import models
from apps.clients.models import Client


class RAGDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ("PROFILE", "Business Profile"),
        ("LOCATION", "Location / Address"),
        ("TIMINGS", "Business Timings"),
        ("SERVICES", "Services / Categories"),
        ("POLICY", "Policies"),
        ("FAQ", "FAQ"),
        ("OTHER", "Other"),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="rag_documents"
    )

    doc_type = models.CharField(
        max_length=50,
        choices=DOC_TYPE_CHOICES
    )

    title = models.CharField(max_length=255)
    content = models.TextField()

    # Lightweight metadata for filtering later
    tags = models.JSONField(default=list, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["client", "doc_type"]),
        ]

    def __str__(self):
        return f"{self.client.name} | {self.doc_type} | {self.title}"
