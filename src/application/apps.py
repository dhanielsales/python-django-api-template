from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    """Application configuration for the application app."""

    name = "application"
