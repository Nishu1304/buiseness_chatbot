from django.contrib import admin
from django.utils import timezone

from apps.scheduler.models import ScheduledMessage
from apps.scheduler.services.manual_trigger import trigger_campaign
from apps.scheduler.services.recipient_selector import (
    get_last_month_customers_mock,
)


@admin.register(ScheduledMessage)
class ScheduledMessageAdmin(admin.ModelAdmin):
    list_display = (
        "message_type",
        "phone",
        "status",
        "scheduled_at",
        "sent_at",
    )

    list_filter = ("status", "message_type", "client")
    search_fields = ("phone", "message_text")

    actions = ["send_feedback_campaign", "run_scheduler_now"]

    @admin.action(description="📣 Send Feedback Campaign (Last Month Customers)")
    def send_feedback_campaign(self, request, queryset):
        client = request.user.client if hasattr(request.user, "client") else None

        if not client:
            self.message_user(request, "No client associated", level="error")
            return

        recipients = get_last_month_customers_mock()

        trigger_campaign(
            client=client,
            recipients=recipients,
            message_type="FEEDBACK",
            message_text=(
                "⭐ We’d love your feedback!\n"
                "Please reply *feedback* to rate your experience."
            ),
            delay_minutes=1,
        )

        self.message_user(
            request,
            f"Feedback campaign scheduled for {len(recipients)} customers",
        )

    @admin.action(description="🚀 Run Scheduler Now")
    def run_scheduler_now(self, request, queryset):
        from apps.scheduler.management.commands.run_scheduler import Command

        Command().handle()

        self.message_user(request, "Scheduler executed successfully")
