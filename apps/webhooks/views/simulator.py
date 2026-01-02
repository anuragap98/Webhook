from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import WebhookEndpoint, WebhookEvent
from ..services.payloads import generate_event_payload
from ..services.sender import send_webhook


def create_event(request):
    endpoints = WebhookEndpoint.objects.filter(is_active=True)

    if request.method == "POST":
        event_type = request.POST["event_type"]
        endpoint_id = request.POST["endpoint"]

        try:
            endpoint = WebhookEndpoint.objects.get(id=endpoint_id)
            payload = generate_event_payload(event_type)

            event = WebhookEvent.objects.create(
                event_type=event_type,
                payload=payload,
            )

            send_webhook(endpoint, event)
            messages.success(
                request, f"Webhook sent to {endpoint.url} with status: {event.status}"
            )
        except WebhookEndpoint.DoesNotExist:
            messages.error(request, "Selected endpoint not found.")
        except Exception as e:
            messages.error(request, f"Error sending webhook: {str(e)}")

        return redirect("create_event")

    return render(
        request,
        "webhooks/create_event.html",
        {"endpoints": endpoints},
    )
