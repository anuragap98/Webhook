from rest_framework import serializers


class WebhookPayloadSerializer(serializers.Serializer):
    event = serializers.CharField()
    data = serializers.DictField()
    timestamp = serializers.DateTimeField()
