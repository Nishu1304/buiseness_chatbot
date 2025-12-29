from datetime import date
from calendar import monthrange
from integrations.bos.factory import get_bos_client
#from apps.analytics.services.bos_client import BOSClient
from apps.analytics.services.aggregations import (
    aggregate_monthly_sales,
    aggregate_feedback,
)
from apps.analytics.services.summarizer import summarize_report
from apps.common.messages import ChatMessage


def handle_monthly_report(client):
    today = date.today()
    start_date = today.replace(day=1)
    end_date = today.replace(day=monthrange(today.year, today.month)[1])

    bos = get_bos_client()
    bills = bos.get_bills_by_date_range(start_date, end_date)

    sales_data = aggregate_monthly_sales(bills)
    feedback_data = aggregate_feedback(client, start_date, end_date)

    combined = {
        "sales": sales_data,
        "feedback": feedback_data,
    }

    summary = summarize_report(combined, today.strftime("%B %Y"))

    return ChatMessage(text=summary)
