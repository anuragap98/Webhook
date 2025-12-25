# Webhook (Django) 🐍

> A small, well-structured Django project demonstrating an "apps/" layout, tests, and CI with formatting & linting hooks.

---

## Table of contents 📚
- [Overview](#overview)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Local development](#local-development)
- [Environment & settings](#environment--settings)
- [Testing](#testing)
- [Formatting & linting (pre-commit)](#formatting--linting-pre-commit)
- [CI (GitHub Actions)](#ci-github-actions)
- [Database migrations](#database-migrations)
- [Admin site](#admin-site)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License & contact](#license--contact)

---

## Overview

This repository is a Django project (Django 4.2.x) organized with application code under the `apps/` package (e.g. `apps/hello`). It includes
- app-level unit tests
- Black and Ruff for formatting & linting
- pre-commit configuration to enforce style locally
- a GitHub Actions workflow that runs pre-commit and tests on pushes/PRs

This README guides you through setting up the project locally, running tests, and contributing.

---

## Architecture

- Root project: `webhook/` (Django project settings & URL config)
- Applications: `apps/hello/` (example app)
- Migrations live under each app in `apps/<app>/migrations/`
- Static & template files follow Django conventions under each app (e.g. `apps/hello/templates/hello/`)

Code style: prefer relative imports inside apps (e.g., `from .models import MyModel`) and register apps in `INSTALLED_APPS` using the full package path (e.g., `'apps.hello'`).

---

## Requirements

- macOS / Linux / Windows with Python 3.14 (compatible with 3.10+)
- Git (recommended for pre-commit hooks and CI)

---

## Local development

1. Create & activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # or: .venv/bin/activate
```

2. Install dependencies

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

3. Create a local `.env` from the example (optional)

```bash
cp .env.example .env
# edit .env as needed
```

4. Run database migrations (development DB)

```bash
python manage.py migrate
```

5. Create an admin user (optional)

```bash
python manage.py createsuperuser
```

6. Run the dev server

```bash
python manage.py runserver
# visit http://127.0.0.1:8000/
```

---

## Environment & settings

This project uses environment-specific settings under `webhook/settings/`:

- `base.py`: common settings
- `dev.py`: development defaults (DEBUG=True)
- `prod.py`: production hardening (SECURE_* settings, Sentry, etc.)
- `test.py`: test settings (in-memory DB, fast hashers)

Switch environments via the `DJANGO_SETTINGS_ENV` environment variable. Example for running with the test settings locally:

```bash
export DJANGO_SETTINGS_ENV=test
python manage.py test
```

Key points:
- Add apps to `INSTALLED_APPS` using their package path, e.g. `"apps.hello"`.
- Use environment variables for secrets (see `.env.example`).

---

## Testing

- Run all tests:

```bash
python manage.py test
```

- Run tests for a single app (faster):

```bash
python manage.py test apps.hello
```

Note: `webhook/settings/test.py` uses an in-memory SQLite DB and faster password hashing to keep tests fast.

---

## Formatting & linting (pre-commit) 🔧

We use **Black** and **Ruff** and enforce them with **pre-commit**.

- Install tools into your virtualenv:

```bash
pip install black ruff pre-commit
```

- Install Git hooks (requires the repo to be a Git repository):

```bash
.venv/bin/pre-commit install
```

- Run hooks across the repo:

```bash
.venv/bin/pre-commit run --all-files
# or run tools individually
.venv/bin/black .
.venv/bin/python -m ruff check --fix .
```

CI also runs these checks automatically on pushes and pull requests.

---

## CI (GitHub Actions)

A workflow is added at `.github/workflows/ci.yml`. It:
- checks out code
- sets up Python 3.14
- installs dependencies
- runs pre-commit hooks (format/lint)
- applies migrations using the `test` settings
- runs `python manage.py test`

You can extend it to run coverage reports or matrixed testing across Python versions.

---

## Database migrations

- Create migrations after model changes:

```bash
python manage.py makemigrations
```

- Apply migrations:

```bash
python manage.py migrate
```

- If you need to reset local migrations during development, prefer a careful approach; do not force-drop production DBs.

---

## Admin site

Visit `/admin/` after creating a superuser with `python manage.py createsuperuser`.

---

## Troubleshooting

- `ModuleNotFoundError: No module named 'django'` → activate `.venv` or install dependencies into the venv.
- `pre-commit` errors during `install` → make sure the repo is initialized with `git init` and that Git is available.
- Tests failing after refactor → ensure imports are relative inside apps and `INSTALLED_APPS` uses full package paths like `apps.hello`.

---

## Contributing

- Run formatters & linters locally (`pre-commit`) and ensure tests pass before opening PRs.
- Keep changes small and add tests for bug fixes and new features.

> Tip: run `python -m pytest -q` or `python manage.py test` locally before pushing.

---

## License & contact

This project is open for learning and experimentation. If you want me to add a formal license file (e.g., MIT), tell me which license to use and I’ll add it.

If you want any additional sections (architecture diagram, API docs, or developer guidelines), I can add them next.
