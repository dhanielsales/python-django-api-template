# mypy: ignore-errors
# pyright: ignore
# type: ignore
# ruff: noqa: F403, D101, ANN204, ANN001, D105, S105

"""Test settings for Django project."""

from typing import Any

# Enable django-stubs
import django_stubs_ext

from .settings import *

# Enable django-stubs
django_stubs_ext.monkeypatch()

# Use in-memory SQLite for tests
DATABASES: dict[str, dict[str, Any]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "OPTIONS": {
            "timeout": 20,
        },
    }
}


# Disable migrations for faster tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Test-specific settings
SECRET_KEY = "test-secret-key-for-testing-only"
DEBUG = False
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",  # Faster for tests
]

# Disable logging during tests
LOGGING_CONFIG = None
