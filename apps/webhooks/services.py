def process_webhook(event: str, data: dict) -> None:
    """
    Central webhook dispatcher
    """
    if event == "order.created":
        handle_order_created(data)
    elif event == "payment.success":
        handle_payment_success(data)
    else:
        raise ValueError(f"Unhandled webhook event: {event}")


def handle_order_created(data: dict) -> None:
    from apps.users.models import Users

    Users.objects.create(
        external_id=data["id"],
        amount=data["amount"],
    )


def handle_payment_success(data: dict) -> None:
    from apps.users.models import Users

    Users.objects.filter(external_id=data["id"]).update(status="paid")
