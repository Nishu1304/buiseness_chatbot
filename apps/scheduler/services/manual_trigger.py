from django.utils import timezone
from datetime import timedelta

from apps.scheduler.models import ScheduledMessage


def trigger_campaign(
    *,
    client,
    recipients,   # [{"phone": "..."}]
    message_type,
    message_text,
    delay_minutes=0,
):
    scheduled_at = timezone.now() + timedelta(minutes=delay_minutes)

    created = 0
    for r in recipients:
        ScheduledMessage.objects.create(
            client=client,
            phone=r["phone"],
            message_type=message_type,
            message_text=message_text,
            scheduled_at=scheduled_at,
        )
        created += 1

    return created
