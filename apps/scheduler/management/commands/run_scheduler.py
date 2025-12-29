from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.scheduler.models import ScheduledMessage
from apps.common.messages import ChatMessage
from apps.whatsapp.senders import send_whatsapp_message

class Command(BaseCommand):
    help = "Send scheduled WhatsApp messages"

    def handle(self, *args, **options):
        now = timezone.now()

        messages = ScheduledMessage.objects.filter(
            status="PENDING",
            scheduled_at__lte=now,
        )

        self.stdout.write(f"Found {messages.count()} messages")

        for msg in messages:
            try:
                send_whatsapp_message(
                    to=msg.phone,
                    message=ChatMessage(text=msg.message_text),
                )

                msg.status = "SENT"
                msg.sent_at = timezone.now()
                msg.error = None

            except Exception as e:
                msg.status = "FAILED"
                msg.error = str(e)

            msg.save()
