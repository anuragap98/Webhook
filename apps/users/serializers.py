# If using DRF, add serializers here
try:
    from rest_framework import serializers
except Exception:  # pragma: no cover - optional dep
    serializers = None


if serializers:
    from django.contrib.auth import get_user_model

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ("id", "username", "email")
