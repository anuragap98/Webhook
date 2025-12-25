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
