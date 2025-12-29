from apps.conversations.models import ConversationSession

SESSION_TTL_MINUTES = 15


def get_session(client, phone):
    session, _ = ConversationSession.objects.get_or_create(
        client=client,
        user_phone=phone,
        defaults={"state": None, "context": {}}
    )

    if session.is_expired(SESSION_TTL_MINUTES):
        session.state = None
        session.context = {}
        session.save(update_fields=["state", "context", "updated_at"])

    return session


def save_session(session, state=None, context=None):
    if state is not None:
        session.state = state
    if context is not None:
        session.context = context

    session.save(update_fields=["state", "context", "updated_at"])


def clear_session(session):
    session.state = None
    session.context = {}
    session.save(update_fields=["state", "context", "updated_at"])
