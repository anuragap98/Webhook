from django.shortcuts import render
from ..models import WebhookEvent, WebhookLog


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect("/admin/")

    # Metrics
    total_events = WebhookEvent.objects.count()

    success_count = WebhookEvent.objects.filter(
        status__in=["processed", "sent"]
    ).count()

    failure_count = WebhookEvent.objects.filter(
        status__in=["failed", "processing_failed"]
    ).count()

    success_rate = 0
    if total_events > 0:
        success_rate = round((success_count / total_events) * 100, 1)

    pending_count = total_events - success_count - failure_count

    # Recent activity
    recent_events = WebhookEvent.objects.order_by("-created_at")[:5]
    logs = WebhookLog.objects.select_related("event").order_by("-created_at")[:50]

    return render(
        request,
        "webhooks/dashboard.html",
        {
            "metrics": {
                "total": total_events,
                "success_count": success_count,
                "failure_count": failure_count,
                "success_rate": success_rate,
                "pending_count": pending_count,
            },
            "recent_events": recent_events,
            "logs": logs,
        },
    )
