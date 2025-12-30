import uuid
import time
import random


def generate_event_payload(event_type: str) -> dict:
    common_data = {
        "event": event_type,
        "timestamp": int(time.time()),
    }

    if event_type == "order.created":
        data = {
            "id": f"ord_{uuid.uuid4().hex[:12]}",
            "amount": float(random.randrange(100, 10000, 50)),
            "currency": "INR",
            "status": "pending",
            "items": [
                {"item_id": 1, "quantity": 1},
                {"item_id": 2, "quantity": 2},
            ],
        }
    elif event_type.startswith("payment."):
        # Generate a consistent order ID so it might match (for testing we might need state but random is fine for basic flow)
        # Ideally we'd query an existing order but let's just make it standalone valid
        data = {
            "id": f"pay_{uuid.uuid4().hex[:12]}",
            # Include order_id so our service logic works if we had an order.
            # For now, if we generate a payment for a non-existent order, the service might log it or ignore it.
            # To make testing easier, maybe we should reuse an order ID if we can, but let's start simple.
            "order_id": f"ord_{uuid.uuid4().hex[:12]}",
            "amount": float(random.randrange(100, 10000, 50)),
            "currency": "INR",
            "status": event_type.split(".")[1] if "." in event_type else "unknown",
            "method": "card",
        }
    else:
        data = {"id": f"evt_{uuid.uuid4().hex[:12]}", "info": "Generic event data"}

    common_data["data"] = data
    return common_data


# Alias for backward compatibility if needed, though we'll update the caller.
generate_payment_payload = generate_event_payload
