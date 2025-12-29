from django.shortcuts import render
from ..models import WebhookEvent, WebhookLog


def dashboard(request):
    events = WebhookEvent.objects.order_by("-created_at")[:20]
    logs = WebhookLog.objects.select_related("event").order_by("-created_at")[:50]
    return render(
        request,
        "webhooks/dashboard.html",
        {
            "events": events,
            "logs": logs,
        },
    )
