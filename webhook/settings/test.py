# ruff: noqa: F403,F405
from .base import *
from decouple import config

# Test settings
SECRET_KEY = config("SECRET_KEY", default="test-secret")
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Use in-memory sqlite for faster unit tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Make password hashing faster during tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
