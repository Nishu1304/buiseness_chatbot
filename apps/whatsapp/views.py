import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from apps.whatsapp.parsers import parse_whatsapp_payload
from apps.whatsapp.senders import send_whatsapp_message
from apps.clients.models import Client, ClientFeature
from apps.conversations.services.session_manager import get_session, save_session
from apps.conversations.services.state_router import route_message

@csrf_exempt
def whatsapp_webhook(request):
    print("➡️ WhatsApp webhook hit | method:", request.method)

    # Meta verification
    if request.method == "GET":
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        print("🔐 Verify token received:", token)

        if token == settings.WHATSAPP_VERIFY_TOKEN:
            print("✅ Webhook verification success")
            return HttpResponse(challenge)

        print("❌ Webhook verification failed")
        return HttpResponse("Invalid token", status=403)

    # Incoming message
    try:
        payload = json.loads(request.body or "{}")
        print("📦 Payload received")
    except json.JSONDecodeError:
        print("❌ Invalid JSON payload")
        return JsonResponse({"status": "invalid json"}, status=400)

    parsed = parse_whatsapp_payload(payload)
    print("🧩 Parsed payload:", parsed)

    if not parsed or not parsed.get("text"):
        print("⚠️ Message ignored (no text)")
        return JsonResponse({"status": "ignored"})

    print(
        "💬 Incoming message | from:",
        parsed["from"],
        "| phone_number_id:",
        parsed["phone_number_id"],
        "| text:",
        parsed["text"]
    )

    try:
        client = Client.objects.get(
            whatsapp_number=parsed["phone_number_id"],
            is_active=True
        )
        features = ClientFeature.objects.get(client=client)
        print("🏫 Client found | client_id:", client.id)
    except Client.DoesNotExist:
        print("❌ Unknown client | phone_number_id:", parsed["phone_number_id"])
        return JsonResponse({"status": "unknown client"})
    except ClientFeature.DoesNotExist:
        print("❌ ClientFeature missing | client_id:", client.id)
        return JsonResponse({"status": "client config error"}, status=500)

    session = get_session(client, parsed["from"])
    print(
        "🧠 Session loaded | session_id:",
        session.id,
        "| state:",
        session.state
    )

    try:
        reply = route_message(parsed["text"], session, features, client)
        print("🧭 Message routed successfully")
    except Exception as e:
        print("🔥 Error routing message:", str(e))
        return JsonResponse({"status": "processing error"}, status=500)

    save_session(session, state=session.state, context=session.context)
    print("💾 Session saved")

    send_whatsapp_message(parsed["from"], reply)
    print("📤 Reply sent to:", parsed["from"])

    return JsonResponse({"status": "ok"})
