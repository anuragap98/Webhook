# If using DRF, add serializers here
try:
    from rest_framework import serializers
except Exception:  # pragma: no cover - optional dep
    serializers = None


if serializers:
    from django.contrib.auth import get_user_model
    from .models import Profile

    User = get_user_model()

    class ProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ("bio",)

    class UserSerializer(serializers.ModelSerializer):
        profile = ProfileSerializer(read_only=True)

        class Meta:
            model = User
            fields = ("id", "username", "email", "profile")

    class RegistrationSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True)
        email = serializers.EmailField(required=True)

        class Meta:
            model = User
            fields = ("id", "username", "email", "password")

        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
            )
            return user
