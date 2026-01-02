from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class UserAPITests(APITestCase):
    def test_registration(self):
        url = reverse("users:api_register")
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "newuser")

    def test_login(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        url = reverse("users:api_login")
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if profile was created via signal
        self.assertTrue(hasattr(user, "profile"))

    def test_profile_api(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.client.force_login(user)
        url = reverse("users:api_profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("bio", response.data)
