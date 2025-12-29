from django.shortcuts import render
from ..models import WebhookEndpoint, WebhookEvent
from ..services.payloads import generate_payment_payload
from ..services.sender import send_webhook


def create_event(request):
    endpoints = WebhookEndpoint.objects.filter(is_active=True)
    result = None

    if request.method == "POST":
        event_type = request.POST["event_type"]
        endpoint_id = request.POST["endpoint"]

        endpoint = WebhookEndpoint.objects.get(id=endpoint_id)
        payload = generate_payment_payload(event_type)

        event = WebhookEvent.objects.create(
            event_type=event_type,
            payload=payload,
        )

        try:
            send_webhook(endpoint, event)
            result = f"Webhook sent to {endpoint.url} with status: {event.status}"
        except Exception as e:
            result = f"Error sending webhook: {str(e)}"

    return render(
        request,
        "webhooks/create_event.html",
        {"endpoints": endpoints, "result": result},
    )
