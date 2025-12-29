from apps.common.messages import ChatMessage
from apps.features.feedback.models import Feedback


def start_feedback(session):
    session.state = "FEEDBACK_RATING"
    session.context = {}
    session.save()

    return ChatMessage(
        text=(
            "⭐ We’d love your feedback!\n\n"
            "Please rate your experience from 1 to 5.\n"
            "(1 = Very bad, 5 = Excellent)"
        )
    )


def handle_feedback_state(session, text, client):
    # STEP 1 — Rating
    if session.state == "FEEDBACK_RATING":
        if not text.isdigit() or not (1 <= int(text) <= 5):
            return ChatMessage(text="Please reply with a number between 1 and 5.")

        session.context["rating"] = int(text)
        session.state = "FEEDBACK_COMMENT"
        session.save()

        return ChatMessage(
            text=(
                "Thank you! 😊\n"
                "Would you like to add a comment? (Optional)\n"
                "Type your message or reply *skip*."
            )
        )

    # STEP 2 — Comment
    if session.state == "FEEDBACK_COMMENT":
        comment = None if text.lower() == "skip" else text.strip()

        Feedback.objects.create(
            client=client,
            phone=session.user_phone,
            rating=session.context["rating"],
            comment=comment,
        )

        session.state = None
        session.context = {}
        session.save()

        return ChatMessage(
            text=(
                "🙏 Thank you for your feedback!\n"
                "It really helps us improve.\n\n"
                "Type *menu* to continue."
            )
        )

    return None
