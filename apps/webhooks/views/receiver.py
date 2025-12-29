from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def webhook_receiver(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    try:
        # payload = json.loads(request.body)
        # Signature validation will be added later
        return JsonResponse({"status": "ok"})
    except Exception:
        return HttpResponseBadRequest("Invalid payload")
