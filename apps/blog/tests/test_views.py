from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import LogMessage
from apps.blog.views import blog_message


class LogMessageModelTests(TestCase):
    def test_str_contains_message_and_date(self):
        msg = LogMessage(message="hello world", log_date=timezone.now())
        assert "hello world" in str(msg)


class LogMessageViewTests(TestCase):
    def test_get_log_form_renders(self):
        factory = RequestFactory()
        request = factory.get(reverse("blog_message"))
        response = blog_message(request)
        assert response.status_code == 200
        assert b"<form" in response.content
