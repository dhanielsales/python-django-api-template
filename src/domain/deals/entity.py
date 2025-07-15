from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field

from core.models import DealModel


class DealEntity(BaseModel):
    """Represents a deal entity with its attributes."""

    id: int
    title: str
    company_id: int
    distributor_id: int | None
    tags: list[int] | None
    value: Annotated[Decimal, Field(gt=0)]

    def __str__(self) -> str:
        """Return the string representation of the deal."""
        return f"{self.title} ({self.company_id})"

    @staticmethod
    def from_model(model: DealModel) -> "DealEntity":
        """Create a DealEntity from a model instance."""
        if not model.company or model.company and not model.company.id:
            raise ValueError("Company must be associated with the deal.")

        return DealEntity(
            id=model.id,
            title=model.title,
            company_id=model.company.id,
            distributor_id=model.distributor.id if model.distributor else None,
            tags=[tag.id for tag in model.tags.all()],
            value=model.value,
        )
