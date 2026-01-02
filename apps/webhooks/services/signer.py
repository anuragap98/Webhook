import hmac
import hashlib
import json
import time


def generate_signature(payload: dict, secret: str) -> str:
    timestamp = str(int(time.time()))
    signed_payload = f"{timestamp}.{json.dumps(payload)}"

    signature = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256,
    ).hexdigest()

    return f"t={timestamp},v1={signature}"
