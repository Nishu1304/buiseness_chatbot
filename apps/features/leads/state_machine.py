import re
from apps.features.leads.models import Lead


EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"


def handle_lead_state(session, text, client):
    state = session.state
    context = session.context

    # STEP 1 — Capture Name
    if state == "LEAD_NAME":
        context["name"] = text.strip()
        session.state = "LEAD_EMAIL"
        session.context = context
        session.save()
        return "Thanks 😊 Please share your email address (or type skip)."

    # STEP 2 — Capture Email
    if state == "LEAD_EMAIL":
        email = text.strip().lower()

        if email != "skip" and not re.match(EMAIL_REGEX, email):
            return "Please enter a valid email or type skip."

        Lead.objects.update_or_create(
            client=client,
            phone=session.user_phone,
            defaults={
                "name": context.get("name"),
                "email": None if email == "skip" else email,
            },
        )

        # Clear session
        session.state = None
        session.context = {}
        session.save()

        return "✅ Thank you! Your details have been saved."

    return None
