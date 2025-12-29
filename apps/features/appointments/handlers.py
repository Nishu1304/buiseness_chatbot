def start_appointment(session):
    session.state = "APPT_SERVICE"
    session.context = {}
    session.save()

    return "Sure 👍 What service would you like to book?"
