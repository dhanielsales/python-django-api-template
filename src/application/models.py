from django.db import models


class FooModel(models.Model):
    """Represents a foo entity with basic information and timestamps."""

    name: "models.CharField[str, str]" = models.CharField(max_length=255)

    def __str__(self) -> str:
        """Return the string representation of the foo (its name)."""
        return self.name
