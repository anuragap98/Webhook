# Django Project 🐍

## Overview
This repository contains a Django project. This README explains how to set up the project's virtual environment, install dependencies, run migrations, and start the dev server.

---

## Requirements
- macOS
- Python 3.14 (or compatible Python 3.10+) installed and available as `python3`

---

## Quick start (recommended)
1. Create and activate a virtual environment

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # zsh / bash
   ```

   If you prefer not to activate the venv, you can run commands directly with `.venv/bin/python` or `.venv/bin/pip`.

2. Upgrade pip and install dependencies

   ```bash
   python -m pip install --upgrade pip setuptools wheel
   pip install "Django>=4.2,<5"
   ```

   or 
   run the below command to install using `requirement.txt`
   ```bash
   pip install -r requirements.txt
   ``` 

3. Run database migrations

   ```bash
   python manage.py migrate
   ```

4. Start the development server

   ```bash
   python manage.py runserver
   # or from host: .venv/bin/python manage.py runserver 0.0.0.0:8000
   ```

5. Open your browser at `http://127.0.0.1:8000/` to view the site.

---

## Useful commands
- Show installed Django version:

  ```bash
  python -c "import django; print(django.get_version())"
  ```

- Run the shell with Django loaded:

  ```bash
  python manage.py shell
  ```

- Create an admin user:

  ```bash
  python manage.py createsuperuser
  ```

- Run tests:

  ```bash
  python manage.py test
  ```

- Make migrations:
    1. Make changes to the models in your models.py file.
    2. Run `python manage.py makemigrations` to generate scripts in the migrations folder that migrate the database from its current state to the new state.
        ```bash
        python manage.py makemigrations
        ```
    3. Run `python manage.py migrate` to apply the scripts to the actual database.
    ---

## Notes
- This project uses a local `.venv` directory by convention. If you use a different environment manager (pyenv, conda, etc.), adapt the activation steps accordingly.
- If you see `ModuleNotFoundError: No module named 'django'`, make sure you have the venv activated or that Django is installed for the Python interpreter you're using.
- App layout: application code lives under the `apps/` package (for example `apps/hello`). Add apps to `INSTALLED_APPS` using the full package path (for example: `'apps.hello'`), and prefer relative imports inside app modules (for example: `from .models import MyModel`).
- Run tests for a single app with `python manage.py test apps.<appname>` (e.g. `python manage.py test apps.hello`).

- To enable pre-commit hooks (Black/Ruff), make sure the repo is a Git repository and then run:

  ```bash
  .venv/bin/pre-commit install
  .venv/bin/pre-commit run --all-files
  ```

  If you don't use Git locally, you can still run Black (`.venv/bin/black .`) and Ruff (`.venv/bin/python -m ruff check --fix .`) manually.

## Production environment variables 🔐

When deploying to production, set the following environment variables (e.g., in a `.env` file or your host's secret manager):

- `DJANGO_SETTINGS_ENV=prod` (loads `webhook.settings.prod`)
- `SECRET_KEY` — **required**. Use a long, random value. Never commit this to source control.
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` — database credentials.
- `ALLOWED_HOSTS` — comma-separated hostnames (e.g., `example.com,www.example.com`).
- `CSRF_TRUSTED_ORIGINS` — comma-separated origins for CSRF checks (e.g., `https://example.com`).
- `SECURE_HSTS_SECONDS` — HSTS max age (default: `31536000`).
- `SECURE_HSTS_INCLUDE_SUBDOMAINS` — `True`/`False`.
- `SECURE_HSTS_PRELOAD` — `True`/`False`.
- `SENTRY_DSN` — optional; set to enable Sentry error reporting.
- `SENTRY_TRACES_SAMPLE_RATE` — optional; set tracing sample rate (e.g., `0.0` or `0.1`).

You can copy `.env.example` and fill values for your deployment:

```bash
cp .env.example .env
# then edit .env and set secrets
```

