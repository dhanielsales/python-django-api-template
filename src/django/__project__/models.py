from datetime import datetime

from django.db import models


class BaseModel(models.Model):
    """Abstract base model for all Django models in the application."""

    class Meta:
        """Meta options for the BaseModel."""

        abstract = True


class TimestampedBaseModel(BaseModel):
    """Abstract base model that provides created and updated timestamps."""

    created_at = models.DateTimeField[datetime, datetime](auto_now_add=True)
    updated_at = models.DateTimeField[datetime, datetime](auto_now=True)


class CompanyModel(TimestampedBaseModel):
    """Represents a company entity with basic information and timestamps."""

    name = models.CharField[str, str](max_length=255)
    address = models.TextField[None, str](blank=True)

    def __str__(self) -> str:
        """Return the string representation of the company (its name)."""
        return self.name


class TagModel(BaseModel):
    """Represents a tag that can be associated with deals."""

    name = models.CharField[str, str](max_length=100, unique=True)

    def __str__(self) -> str:
        """Return the string representation of the tag (its name)."""
        return self.name


class DistributorModel(BaseModel):
    """Represents a distributor entity with contact information."""

    name = models.CharField[str, str](max_length=255)
    contact_email = models.EmailField[None, str](blank=True)

    def __str__(self) -> str:
        """Return the string representation of the distributor (its name)."""
        return self.name


class DealModel(TimestampedBaseModel):
    """Represents a deal, linking companies, distributors, tags, and value."""

    title = models.CharField[str, str](max_length=255)
    company = models.ForeignKey[CompanyModel, CompanyModel](
        CompanyModel, on_delete=models.CASCADE, related_name="deals"
    )
    distributor = models.ForeignKey[None, DistributorModel](
        DistributorModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deals",
    )
    tags = models.ManyToManyField[TagModel, TagModel](
        TagModel, blank=True, related_name="deals"
    )
    value = models.DecimalField[float, float](max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        """Return the string representation of the deal (its title)."""
        return self.title
