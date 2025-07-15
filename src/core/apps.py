from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    """Configuration for the app application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"  # This should match your app directory name
    verbose_name = "Project App"  # Optional: human-readable name
