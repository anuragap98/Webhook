"""Environment-based settings package initializer for webhook.

This module picks one of the env-specific settings modules
(`dev`, `prod`, `test`) based on `DJANGO_SETTINGS_ENV` and
re-exports its symbols so `import webhook.settings` continues
to work and Django can import settings normally.
"""

from decouple import config

ENV = config("DJANGO_SETTINGS_ENV", default="dev").lower()

if ENV == "prod":
    from .prod import *  # noqa: F401,F403
elif ENV == "test":
    from .test import *  # noqa: F401,F403
else:
    # default to 'dev'
    from .dev import *  # noqa: F401,F403
