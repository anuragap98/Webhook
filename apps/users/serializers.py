from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for User Profile data."""

    class Meta:
        model = Profile
        fields = ("bio",)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User and nested Profile data."""

    profile = ProfileSerializer(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "profile", "date_joined", "is_staff")
        read_only_fields = ("id", "date_joined", "is_staff")


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration via API."""

    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
