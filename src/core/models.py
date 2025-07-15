from datetime import datetime
from decimal import Decimal

from django.db import models


class BaseModel(models.Model):
    """Abstract base model for all Django models in the application."""

    id: int
    created_at: "models.DateTimeField[datetime, datetime]" = models.DateTimeField(
        auto_now_add=True
    )
    updated_at: "models.DateTimeField[datetime, datetime]" = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        """Meta options for the BaseModel."""

        abstract = True


class CompanyModel(BaseModel):
    """Represents a company entity with basic information and timestamps."""

    name: "models.CharField[str, str]" = models.CharField(max_length=255)
    address: "models.TextField[str, str | None]" = models.TextField(
        blank=True, null=True
    )  # Demonstrate this

    def __str__(self) -> str:
        """Return the string representation of the company (its name)."""
        return self.name


class TagModel(BaseModel):
    """Represents a tag that can be associated with deals."""

    name: "models.CharField[str, str]" = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        """Return the string representation of the tag (its name)."""
        return self.name


class DistributorModel(BaseModel):
    """Represents a distributor entity with contact information."""

    name: "models.CharField[str, str]" = models.CharField(max_length=255)
    contact_email: "models.EmailField[str, str]" = models.EmailField(blank=True)

    def __str__(self) -> str:
        """Return the string representation of the distributor (its name)."""
        return self.name


class DealModel(BaseModel):
    """Represents a deal, linking companies, distributors, tags, and value."""

    title: "models.CharField[str, str]" = models.CharField(max_length=255)
    company_id: int
    company: "models.ForeignKey[CompanyModel, CompanyModel]" = models.ForeignKey(
        CompanyModel, on_delete=models.CASCADE, related_name="deals"
    )
    distributor_id: int
    distributor: "models.ForeignKey[DistributorModel | None, DistributorModel | None]" = (
        models.ForeignKey(
            DistributorModel,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="deals",
        )
    )
    tags: "models.ManyToManyField[TagModel, TagModel]" = models.ManyToManyField(
        TagModel, blank=True, related_name="deals"
    )
    value: "models.DecimalField[Decimal, Decimal]" = models.DecimalField(
        max_digits=12, decimal_places=2
    )

    def __str__(self) -> str:
        """Return the string representation of the deal (its title)."""
        return self.title
