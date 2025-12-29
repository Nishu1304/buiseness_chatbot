import requests
from apps.common.messages import ChatMessage
from django.conf import settings


WHATSAPP_URL = f"https://graph.facebook.com/v19.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"


def send_whatsapp_message(to, message):
    headers = {
             "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
             "Content-Type": "application/json",
        }
    # 1️⃣ If multiple messages → send one by one
    if isinstance(message, list):
        for msg in message:
            send_whatsapp_message(to, msg)
        return

    # 2️⃣ Normalize ChatMessage → payload
    if isinstance(message, ChatMessage):

        if message.image_url:
            print(f"Recieved till here sending images: {message}" )
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "image",
                "image": {
                    "link": message.image_url,
                    "caption": message.caption or "",
                },
            }
        else:
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": message.text or ""},
            }

    # 3️⃣ Plain text fallback
    elif isinstance(message, str):
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message},
        }
    else:
        raise ValueError(f"Unsupported message type: {type(message)}")

    requests.post(WHATSAPP_URL, headers=headers, json=payload).raise_for_status()

