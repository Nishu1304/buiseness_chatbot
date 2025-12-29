from apps.common.constants import RESET_KEYWORDS
from apps.conversations.services.welcome import get_welcome_message
from apps.conversations.services.menu_router import handle_menu_selection
import requests
from django.conf import settings
from apps.common.messages import ChatMessage
from apps.conversations.intent_registry import INTENTS
from apps.conversations.intent_classifier import classify_intent

from apps.features.leads.state_machine import handle_lead_state
from apps.features.appointments.state_machine import handle_appointment_state
from apps.features.products.state_machine import handle_product_state
from apps.features.feedback.handlers import handle_feedback_state
from apps.analytics.handlers import handle_monthly_report


def route_message(text, session, features, client):
    text_lower = text.lower().strip()

    # 🔒 ADMIN MODE (HIGHEST PRIORITY)
    if session.user_phone == "918011051021":  # client.whatsapp_number: Needs to add a new field this number is the id
        if text_lower in {"hi", "hello", "hey"}:
            return (
                "👋 Hi! You’re logged in as *Store Admin*.\n\n"
                "You can ask:\n"
                "• monthly report\n"
                "• sales summary\n"
                "• this month performance"
            )

        if text_lower in {
            "monthly report",
            "sales report",
            "sales summary",
            "this month performance",
        }:
            return handle_monthly_report(client)

        return (
            "❓ I can help with store reports.\n"
            "Try typing *monthly report*."
        )


    # 0️⃣ Global reset / menu
    if text_lower in RESET_KEYWORDS:
        session.state = None
        session.context = {}
        session.save()
        return get_welcome_message(client)





    # 🔒 1️⃣ PRODUCT STATE MUST HARD-LOCK CONTROL
    if session.state == "PRODUCT_BROWSE":
        response = handle_product_state(session, text)
        if response is not None:
            return response

        # only fallback inside product mode
        return (
            "Type *more* to see more products\n"
            "Type *category* to change category\n"
            "Type *menu* to go back"
        )
    # For feedback state

    if session.state in {"FEEDBACK_RATING", "FEEDBACK_COMMENT"}:
        response = handle_feedback_state(
            session=session,
            text=text,
            client=client,
        )
        if response:
            return response

    # 2️⃣ Other active state machines
    if session.state:
        response = handle_lead_state(session, text, client)
        if response:
            return response

        response = handle_appointment_state(session, text, client)
        if response:
            return response

        return (
            "I didn’t quite understand that.\n"
            "Type *menu* to see options."
        )

    # 3️⃣ Menu numeric selection
    if text_lower.isdigit():
        return handle_menu_selection(text_lower, session, client)

    # 4️⃣ Intent classification (ONLY WHEN NO STATE)
    intent = classify_intent(text, INTENTS)
    if intent:
        return intent.handler(session, client, text)

    # 5️⃣ LLM FREE-TEXT RESPONSE (NO MENU)
    llm_reply = get_general_llm_reply(
        text=text,
        client=client,
    )
    if llm_reply:
        return llm_reply

    # 5️⃣ Safe fallback
    return get_welcome_message(client)




def get_general_llm_reply(text, client):
    prompt = f"""
You are a helpful WhatsApp business assistant.

Rules:
- Be polite and concise
- Do NOT invent prices, offers, or reports
- If user asks for products, bookings, feedback, or reports, guide them politely
- If unsure, suggest typing 'menu'

Business name: {client.name}

User message:
{text}
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
            "max_tokens": 120,
        },
        timeout=10,
    )

    response.raise_for_status()

    reply = response.json()["choices"][0]["message"]["content"].strip()

    if not reply:
        return None

    return ChatMessage(text=reply)