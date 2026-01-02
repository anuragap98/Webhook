from django.test import TestCase
from django.urls import reverse, resolve
from apps.users.views import profile_view


class UsersViewsTests(TestCase):
    def test_profile_route_resolves(self):
        url = reverse("users:profile")
        # Avoid rendering templates here to prevent template-engine copy issues in the test runner.
        self.assertEqual(url, "/users/profile/")
        match = resolve(url)
        self.assertEqual(match.func, profile_view)
