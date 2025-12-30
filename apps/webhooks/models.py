from django.db import models
from django.contrib.auth import get_user_model


class WebhookEndpoint(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="webhook_endpoints",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    url = models.URLField(
        help_text="The URL to which the webhook payloads will be sent."
    )
    secret = models.CharField(
        max_length=255, help_text="Secret used to sign webhook payloads."
    )
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.name} - {self.url} ({'active' if self.is_active else 'inactive'})"
        )


class WebhookEvent(models.Model):
    EVENT_TYPES = [
        ("received", "Received"),
        ("processing", "Processing"),
        ("processed", "Processed"),
        ("order.created", "Order Created"),
        ("order.updated", "Order Updated"),
        ("order.cancelled", "Order Cancelled"),
        ("payment.succeeded", "Payment Succeeded"),
        ("payment.failed", "Payment Failed"),
        ("payment.refunded", "Payment Refunded"),
        ("payment.chargeback", "Payment Chargeback"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("processed", "Processed"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    payload = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} ({self.status})"


# Log model for webhook event delivery attempts
class WebhookLog(models.Model):
    event = models.ForeignKey(
        WebhookEvent, on_delete=models.CASCADE, related_name="logs"
    )
    status = models.CharField(max_length=20)
    response_body = models.TextField(
        blank=True, help_text="Response body from the destination"
    )
    request_headers = models.JSONField(
        default=dict, blank=True, help_text="Headers sent or received"
    )
    message = models.TextField(blank=True, help_text="Human readable summary")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.event.event_type} at {self.created_at} [{self.status}]"
