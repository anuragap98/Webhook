# ruff: noqa: F403,F405
from .base import *
from decouple import config

# Development settings
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-rdc#_2^j7pilre!y(f+&_vk42+j8qk))=*2lo^#0psn7fgrtlv",
)
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Useful during development
INTERNAL_IPS = ["127.0.0.1"]

# Trust local origins for CSRF (Required for Django 4.0+)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
]

# Development Overrides to prevent CSRF "Cookie Not Set" errors locally
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_USE_SESSIONS = False  # Reverting to cookie-based for standard admin compatibility
CSRF_COOKIE_HTTPONLY = False
