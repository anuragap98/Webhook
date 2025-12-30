import requests
from ..models import WebhookLog
from .signer import generate_signature


def send_webhook(endpoint, event):
    signature = generate_signature(event.payload, endpoint.secret)

    headers = {
        "Content-Type": "application/json",
        "Stripe-Signature": signature,
    }

    try:
        response = requests.post(
            endpoint.url,
            json=event.payload,
            headers=headers,
            timeout=5,
        )

        if response.status_code < 400:
            event.status = "sent"
            log_status = "success"
        else:
            event.status = "failed"
            log_status = "failed"

        WebhookLog.objects.create(
            event=event,
            status=log_status,
            request_headers=headers,
            response_body=response.text[:2000],  # Capture more content
            message=f"HTTP {response.status_code}",
        )

    except Exception as e:
        event.status = "failed"
        WebhookLog.objects.create(
            event=event, status="error", request_headers=headers, message=str(e)
        )
    finally:
        event.save()
