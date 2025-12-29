from django.contrib import admin
from .models import RAGDocument


@admin.register(RAGDocument)
class RAGDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "doc_type",
        "title",
        "is_active",
        "updated_at",
    )
    list_filter = ("doc_type", "is_active")
    search_fields = ("title", "content", "client__name")
    ordering = ("-updated_at",)
