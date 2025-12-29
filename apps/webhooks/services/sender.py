import requests
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
        else:
            event.status = "failed"

        event.save()

    except Exception:
        event.status = "failed"
        event.save()
