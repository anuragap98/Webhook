# ruff: noqa: F403,F405
from .base import *
from decouple import config

# Production settings
# SECRET_KEY must be set in the environment for production
SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = [h for h in config("ALLOWED_HOSTS", default="").split(",") if h]

# Security hardening defaults (can be customized per deployment)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True, cast=bool
)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=True, cast=bool)

# Prevent content type sniffing and clickjacking
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Referrer policy
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# If behind a proxy/load balancer, ensure request is marked secure
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Optional: CSRF trusted origins (comma-separated env var)
_CSRF_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="").split(",")
if _CSRF_ORIGINS and _CSRF_ORIGINS != [""]:
    CSRF_TRUSTED_ORIGINS = [u.strip() for u in _CSRF_ORIGINS]

# Content Security Policy (requires `django-csp` package)
# Install: pip install django-csp
# Add `'csp.middleware.CSPMiddleware'` to MIDDLEWARE (inserted automatically below if installed)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "https://fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:")

# Try to register CSP middleware if django-csp is installed
try:
    import importlib

    importlib.import_module("csp.middleware")
    # Prefer placing CSPMiddleware after SecurityMiddleware if present
    if "csp.middleware.CSPMiddleware" not in MIDDLEWARE:
        try:
            idx = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware")
            MIDDLEWARE.insert(idx + 1, "csp.middleware.CSPMiddleware")
        except ValueError:
            MIDDLEWARE.insert(0, "csp.middleware.CSPMiddleware")
except Exception:
    # django-csp not installed; CSP settings will be ignored until installed
    pass

# Security-related headers
SECURE_BROWSER_XSS_FILTER = True

# Logging configuration (console + email on errors when ADMINS is set)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
            "level": "ERROR",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins", "console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# Optional Sentry integration (requires `sentry-sdk`)
SENTRY_DSN = config("SENTRY_DSN", default="")
SENTRY_TRACES_SAMPLE_RATE = config("SENTRY_TRACES_SAMPLE_RATE", default=0.0, cast=float)
if SENTRY_DSN:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[DjangoIntegration()],
            traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
            send_default_pii=False,
        )
    except Exception:
        # If sentry isn't available, fail gracefully; logs will still be emitted
        pass
