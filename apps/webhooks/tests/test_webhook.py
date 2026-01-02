from rest_framework.test import APIClient
from django.test import TestCase


class WebhookTest(TestCase):
    def test_webhook_success(self):
        client = APIClient()
        response = client.post(
            "/webhooks/receive/",
            {
                "event": "order.created",
                "data": {"id": "123", "amount": 100},
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
