def parse_whatsapp_payload(payload: dict):
    """
    Extracts the bare minimum we need from Meta payload.
    Safe against malformed events.
    """
    try:
        entry = payload["entry"][0]
        change = entry["changes"][0]
        value = change["value"]

        message = value["messages"][0]
        phone = message["from"]
        text = message.get("text", {}).get("body", "")

        metadata = value["metadata"]
        business_phone_id = metadata["phone_number_id"]

        return {
            "from": phone,
            "text": text.strip(),
            "phone_number_id": business_phone_id,
        }
    except (KeyError, IndexError):
        return None
