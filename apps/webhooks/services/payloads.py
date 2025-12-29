import uuid
import time


def generate_payment_payload(event_type: str) -> dict:
    return {
        "id": f"evt_{uuid.uuid4().hex[:24]}",
        "type": event_type,
        "created": int(time.time()),
        "data": {
            "object": {
                "id": f"pay_{uuid.uuid4().hex[:24]}",
                "amount": 1999,
                "currency": "INR",
                "status": event_type.split(".")[1],
            }
        },
    }
