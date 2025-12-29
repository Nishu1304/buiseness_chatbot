from django.core.management.base import BaseCommand

from apps.clients.models import Client
from apps.scheduler.services.manual_trigger import trigger_campaign
from apps.scheduler.services.recipient_selector import (
    get_last_month_customers_mock
)


class Command(BaseCommand):
    help = "Send feedback campaign to last month customers"

    def handle(self, *args, **options):
        client = Client.objects.first()

        recipients = get_last_month_customers_mock()

        count = trigger_campaign(
            client=client,
            recipients=recipients,
            message_type="FEEDBACK",
            message_text=(
                "⭐ We’d love your feedback!\n"
                "Please reply *feedback* to rate your experience."
            ),
            delay_minutes=1,
        )

        self.stdout.write(self.style.SUCCESS(
            f"Scheduled {count} feedback messages"
        ))
