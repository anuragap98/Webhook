from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import WebhookPayloadSerializer
from .services import process_webhook


@api_view(["POST"])
@permission_classes([AllowAny])  # Webhooks usually authenticate differently
def webhook_receiver(request):
    serializer = WebhookPayloadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        process_webhook(
            event=serializer.validated_data["event"],
            data=serializer.validated_data["data"],
        )
    except ValueError as exc:
        return Response(
            {"error": str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response({"status": "ok"}, status=status.HTTP_200_OK)
