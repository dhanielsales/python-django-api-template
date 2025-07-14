from datetime import datetime
from decimal import Decimal

from django.__project__.models import (  # type: ignore
    DealModel,
    DistributorModel,
    TagModel,
)
from django.db import transaction

from .entities import DealEntity


class DealRepository:
    """Repository for managing DealModel instances."""

    def __init__(self) -> None:
        """Initialize the DealRepository with a deal manager."""
        self.producer = ""

    def create(
        self,
        title: str,
        company_id: int,
        distributor_id: int | None,
        tags: list[int] | None,
        value: float | None,
    ) -> DealEntity:
        """Create a new deal."""
        deal_model = DealModel.objects.create(
            title=title,
            company_id=company_id,
            distributor_id=distributor_id,
            tags=tags,
            value=value,
        )

        return DealEntity.from_model(deal_model)

    def get_one(self, deal_id: int) -> DealEntity | None:
        """Retrieve a deal by its ID."""
        deal_model = DealModel.objects.filter(id=deal_id).first()

        if deal_model:
            return DealEntity.from_model(deal_model)

        return None

    def get_all(self) -> list[DealEntity]:
        """Retrieve all deals."""
        deal_models = DealModel.objects.all()
        return [DealEntity.from_model(deal) for deal in deal_models]

    @transaction.atomic
    def update(
        self,
        deal_id: int,
        title: str | None,
        distributor_id: int | None,
        tags: list[int] | None,
        value: Decimal | None,
    ) -> DealEntity | None:
        """Update an existing deal."""
        deal = DealModel.objects.filter(id=deal_id).first()
        if not deal:
            raise ValueError(f"Deal with ID {deal_id} does not exist.")

        if title is None:
            title = deal.title

        if value is None:
            value = deal.value

        if tags is None:
            # Delete all tags associated with the deal.
            deleted_tags = deal.tags.all()
            deleted_tags.delete()

            new_tags = TagModel.objects.filter(id__in=tags)
            deal.tags = new_tags

        if distributor_id:
            # Ensure the distributor exists.
            distributor = DistributorModel.objects.filter(id=distributor_id).first()
            if not distributor:
                raise ValueError(f"Distributor with ID {distributor_id} does not exist.")

            deal.distributor = distributor

        # Update the deal attributes.
        deal.updated_at = datetime.now()
        deal.save()

        return DealEntity.from_model(deal)

    def delete(self, deal_id: int) -> bool:
        """Delete a deal by its ID."""
        deal = DealModel.objects.filter(id=deal_id).first()
        if deal:
            deal.delete()
            return True
        return False
