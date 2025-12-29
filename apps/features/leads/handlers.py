def start_lead_capture(session):
    session.state = "LEAD_NAME"
    session.context = {}
    session.save()

    return "Sure 👍 May I know your name?"
