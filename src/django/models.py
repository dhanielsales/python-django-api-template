# mypy: ignore-errors
# pyright: ignore
# type: ignore
# # ruff: noqa: B028, E402
"""Django models module that handles setup and exports models."""

import os
import sys
from pathlib import Path


def _setup_django() -> None:
    """Setup Django for use throughout the project."""
    try:
        # Get Django directory
        django_dir = Path(__file__).parent
        django_dir_str = str(django_dir)

        # Remove any existing references to avoid conflicts
        paths_to_remove = [p for p in sys.path if "src/django" in p or "src\\django" in p]
        for path in paths_to_remove:
            sys.path.remove(path)

        # Add Django directory as the FIRST entry in sys.path
        sys.path.insert(0, django_dir_str)

        # Set Django settings module
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

        # Change to Django directory temporarily
        original_cwd = os.getcwd()
        os.chdir(django_dir)

        try:
            # Setup Django
            import django
            from django.conf import settings

            if not settings.configured:
                django.setup()
            elif not django.apps.apps.ready:
                django.setup()
        finally:
            # Always restore original directory
            os.chdir(original_cwd)

    except Exception as e:
        import warnings

        warnings.warn(f"Django setup error: {e}")


# Setup Django
_setup_django()

# Import and export models
from __project__.models import CompanyModel, DealModel, DistributorModel, TagModel

__all__ = ["DealModel", "DistributorModel", "TagModel", "CompanyModel"]
