from apps.features.appointments.handlers import start_appointment
from apps.features.orders.handlers import handle_purchase_history
from apps.features.faqs.handlers import handle_faq
from apps.features.leads.handlers import start_lead_capture
from apps.features.feedback.handlers import start_feedback  # we’ll stub this
from apps.common.constants import MAIN_MENU_TEXT

def handle_menu_selection(text, session, client):
    choice = text.strip()

    if choice == "1":
        return handle_faq(client, "store info")

    if choice == "2":
        return start_appointment(session)

    if choice == "3":
        return handle_purchase_history(client, session.user_phone)

    if choice == "4":
        return (
            "🛍️ We offer a wide range of products.\n"
            "Popular categories include groceries, daily essentials, and more.\n"
            "Ask me about any product you’re looking for."
        )

    if choice == "5":
        return start_feedback(session)

    if choice == "6":
        return (
            "📞 Our team will assist you shortly.\n"
            "Please share your query."
        )

    return MAIN_MENU_TEXT.format(business_name=client.name)
