from datetime import datetime
from apps.features.appointments.models import Appointment


def handle_appointment_state(session, text, client):
    state = session.state
    context = session.context

    # STEP 1 — Service
    if state == "APPT_SERVICE":
        context["service"] = text.strip()
        session.state = "APPT_DATE"
        session.context = context
        session.save()
        return "📅 Please enter appointment date (YYYY-MM-DD)."

    # STEP 2 — Date
    if state == "APPT_DATE":
        try:
            date = datetime.strptime(text.strip(), "%Y-%m-%d").date()
        except ValueError:
            return "❌ Invalid date format. Please use YYYY-MM-DD."

        context["date"] = str(date)
        session.state = "APPT_TIME"
        session.context = context
        session.save()
        return "⏰ Please enter preferred time (e.g. 4 PM)."

    # STEP 3 — Time
    if state == "APPT_TIME":
        context["time"] = text.strip()
        session.state = "APPT_CONFIRM"
        session.context = context
        session.save()

        return (
            f"✅ Please confirm your appointment:\n\n"
            f"Service: {context['service']}\n"
            f"Date: {context['date']}\n"
            f"Time: {context['time']}\n\n"
            f"Reply YES to confirm or NO to cancel."
        )

    # STEP 4 — Confirmation
    if state == "APPT_CONFIRM":
        if text.lower() == "yes":
            Appointment.objects.create(
                client=client,
                phone=session.user_phone,
                name=context.get("name", "Customer"),
                service=context["service"],
                appointment_date=context["date"],
                appointment_time=context["time"],
                status="CONFIRMED",
            )

            session.state = None
            session.context = {}
            session.save()

            return "🎉 Your appointment is confirmed!"

        if text.lower() == "no":
            session.state = None
            session.context = {}
            session.save()
            return "❌ Appointment cancelled."

        return "Please reply YES or NO."

    return None
