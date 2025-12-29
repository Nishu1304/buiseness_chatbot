from apps.conversations.intents import Intent

from apps.features.appointments.handlers import start_appointment
from apps.features.orders.handlers import handle_purchase_history
from apps.features.leads.handlers import start_lead_capture
from apps.features.faqs.handlers import handle_faq
from apps.features.feedback.handlers import start_feedback
from apps.features.products.handlers import start_product_catalog

INTENTS = [
    Intent(
        name="APPOINTMENT",
        keywords={"appointment", "book", "booking", "meeting"},
        priority=100,
        handler=lambda session, client, text: start_appointment(session),
    ),

    Intent(
        name="PURCHASE_HISTORY",
        keywords={"order", "orders", "bill", "bills", "purchase", "history"},
        priority=90,
        handler=lambda session, client, text: handle_purchase_history(
            client, session.user_phone
        ),
    ),

    Intent(
        name="PRODUCT_CATALOG",
        keywords={"product", "products", "catalog", "items", "shop"},
        priority=85,
        handler=lambda session, client, text: start_product_catalog(session, client),
    ),

    Intent(
        name="LEAD",
        keywords={"contact", "callback", "enquiry", "inquiry"},
        priority=80,
        handler=lambda session, client, text: start_lead_capture(session),
    ),

    Intent(
        name="FEEDBACK",
        keywords={"feedback", "review", "rate"},
        priority=70,
        handler=lambda session, client, text: start_feedback(session),
    ),

    Intent(
        name="FAQ",
        keywords={"time", "timing", "open", "address", "where", "location", "store info"},
        priority=80,
        handler=lambda session, client, text: handle_faq(client, text),
    ),
]
