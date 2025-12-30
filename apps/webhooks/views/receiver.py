import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from ..services.dispatcher import process_webhook
from ..models import WebhookEvent, WebhookLog


@csrf_exempt
def webhook_receiver(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    try:
        payload = json.loads(request.body)
        event_type = payload.get("event", "unknown")

        # 1. Audit Log: Record that we received an event
        webhook_event = WebhookEvent.objects.create(
            event_type=event_type, payload=payload, status="received"
        )

        data = payload.get("data")

        if event_type and data:
            try:
                result_message = process_webhook(event_type, data)

                # 2. Success Log
                webhook_event.status = "processed"
                webhook_event.save()

                WebhookLog.objects.create(
                    event=webhook_event,
                    status="success",
                    request_headers=dict(request.headers),
                    message=result_message,
                )

                return JsonResponse({"status": "ok"})

            except Exception as logic_error:
                # 3. Processing Error Log
                webhook_event.status = "processing_failed"
                webhook_event.save()

                WebhookLog.objects.create(
                    event=webhook_event,
                    status="error",
                    request_headers=dict(request.headers),
                    message=f"Business logic error: {str(logic_error)}",
                )
                return HttpResponseBadRequest(f"Error processing: {str(logic_error)}")
        else:
            return HttpResponseBadRequest("Missing event or data in payload")

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        return HttpResponseBadRequest(f"Error accepting webhook: {str(e)}")
