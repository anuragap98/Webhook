from apps.orders.models import Order, Payment
import uuid


def process_webhook(event: str, data: dict) -> str:
    """
    Central webhook dispatcher
    """
    if event == "order.created":
        return handle_order_created(data)
    elif event == "order.updated":
        return handle_order_updated(data)
    elif event == "order.cancelled":
        return handle_order_cancelled(data)
    elif event in ["payment.success", "payment.succeeded"]:
        return handle_payment_success(data)
    elif event == "payment.failed":
        return handle_payment_failed(data)
    elif event == "payment.refunded":
        return handle_payment_refunded(data)
    elif event == "payment.chargeback":
        return handle_payment_chargeback(data)
    else:
        raise ValueError(f"Unhandled webhook event: {event}")


# --- ORDER HANDLERS ---


def handle_order_created(data: dict) -> str:
    # Use update_or_create to make it idempotent
    order, created = Order.objects.update_or_create(
        external_id=data["id"],
        defaults={
            "amount": data["amount"],
            "currency": data.get("currency", "INR"),
            "status": data.get("status", "pending"),
            "items": data.get("items", []),
        },
    )
    return f"Order {order.external_id} {'created' if created else 'updated'}"


def handle_order_updated(data: dict) -> str:
    # Update arbitrary fields if order exists
    try:
        order = Order.objects.get(external_id=data["id"])
        changes = []

        # Whitelist updatable fields
        if "amount" in data:
            order.amount = data["amount"]
            changes.append("amount")
        if "items" in data:
            order.items = data["items"]
            changes.append("items")

        # Don't update status blindly if it's a specific status transition event
        if "status" in data:
            order.status = data["status"]
            changes.append("status")

        order.save()
        return f"Order {order.external_id} updated: {', '.join(changes)}"
    except Order.DoesNotExist:
        return f"Order {data.get('id')} not found for update"


def handle_order_cancelled(data: dict) -> str:
    rows = Order.objects.filter(external_id=data["id"]).update(status="cancelled")
    return (
        f"Order {data.get('id')} cancelled"
        if rows
        else f"Order {data.get('id')} not found"
    )


# --- PAYMENT HANDLERS ---


def _get_order(data):
    # Helper to resolve order from payload
    order_id = data.get("order_id")
    if not order_id:
        # Fallback to checking if the 'id' itself matches an order (older logic)
        return Order.objects.filter(external_id=data.get("id")).first()
    return Order.objects.filter(external_id=order_id).first()


def handle_payment_success(data: dict) -> str:
    order = _get_order(data)

    if order:
        order.status = "paid"
        order.save()

        payment_id = data.get("payment_id") or data.get("id")
        # Legacy check if ID was reused
        if payment_id == order.external_id:
            payment_id = f"pay_{uuid.uuid4()}"

        Payment.objects.create(
            order=order,
            external_id=payment_id,
            amount=data.get("amount", order.amount),
            currency=data.get("currency", "INR"),
            status="success",
            method=data.get("method", ""),
        )
        return f"Payment {payment_id} recorded for Order {order.external_id}"
    return f"Order not found for payment {data.get('id')}"


def handle_payment_failed(data: dict) -> str:
    order = _get_order(data)
    if order:
        Payment.objects.create(
            order=order,
            external_id=data.get("id", f"fail_{uuid.uuid4().hex[:12]}"),
            amount=data.get("amount", order.amount),
            currency=data.get("currency", "INR"),
            status="failed",
            method=data.get("method", ""),
        )
        return f"Failed payment recorded for Order {order.external_id}"
    return f"Order not found for failed payment {data.get('id')}"


def handle_payment_refunded(data: dict) -> str:
    order = _get_order(data)
    if order:
        order.status = "refunded"
        order.save()

        Payment.objects.create(
            order=order,
            external_id=data.get("id", f"ref_{uuid.uuid4().hex[:12]}"),
            amount=data.get("amount", order.amount),
            currency=data.get("currency", "INR"),
            status="refunded",
            method=data.get("method", ""),
        )
        return f"Order {order.external_id} marked as refunded"
    return "Order not found for refund"


def handle_payment_chargeback(data: dict) -> str:
    order = _get_order(data)
    if order:
        order.status = "disputed"
        order.save()

        Payment.objects.create(
            order=order,
            external_id=data.get("id", f"cb_{uuid.uuid4().hex[:12]}"),
            amount=data.get("amount", order.amount),
            currency=data.get("currency", "INR"),
            status="chargeback",
            method=data.get("method", ""),
        )
        return f"Order {order.external_id} marked as disputed (chargeback)"
    return "Order not found for chargeback"
