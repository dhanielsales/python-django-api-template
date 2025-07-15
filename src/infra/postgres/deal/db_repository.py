from datetime import datetime
from decimal import Decimal

from django.db import transaction

from core.models import DealModel, DistributorModel, TagModel
from domain.deals.entity import DealEntity
from domain.deals.repository import DealRepository


class DealRepositoryDB(DealRepository):
    """Repository for managing DealModel instances."""

    def __init__(self) -> None:
        """Initialize the DealRepository with a deal manager."""
        # Use the default managers for the models.
        # This is necessary to ensure that the repository
        # can interact with the models correctly.
        # Issue: https://github.com/typeddjango/django-stubs/issues/1684#issuecomment-1706446344
        self.deal_manager = DealModel._default_manager
        self.distributor_manager = DistributorModel._default_manager
        self.tags_manager = TagModel._default_manager

    @transaction.atomic
    def create(
        self,
        title: str,
        company_id: int,
        value: Decimal,
        tags: list[int] | None,
        distributor_id: int | None,
    ) -> DealEntity:
        """Create a new deal."""
        deal_model = self.deal_manager.create(
            title=title,
            company_id=company_id,
            distributor_id=distributor_id,
            value=value,
        )

        if tags:
            deal_model.tags.set(tags)

        return DealEntity.from_model(deal_model)

    def get_one(self, deal_id: int) -> DealEntity | None:
        """Retrieve a deal by its ID."""
        deal_model = self.deal_manager.filter(id=deal_id).first()

        if deal_model:
            return DealEntity.from_model(deal_model)

        return None

    def get_all(self) -> list[DealEntity]:
        """Retrieve all deals."""
        deal_models = self.deal_manager.all()
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
        deal = self.deal_manager.filter(id=deal_id).first()
        if not deal:
            raise ValueError(f"Deal with ID {deal_id} does not exist.")

        if title is not None:
            deal.title = title

        if value is not None:
            deal.value = value

        if tags is not None:
            # Delete all tags associated with the deal.
            deleted_tags = deal.tags.all()
            deleted_tags.delete()

            new_tags = self.tags_manager.filter(id__in=tags)
            deal.tags.set(new_tags)

        if distributor_id:
            # Ensure the distributor exists.
            distributor = self.distributor_manager.filter(id=distributor_id).first()
            if not distributor:
                raise ValueError(f"Distributor with ID {distributor_id} does not exist.")

            deal.distributor = distributor

        # Update the deal attributes.
        deal.updated_at = datetime.now()
        deal.save()

        return DealEntity.from_model(deal)

    def delete(self, deal_id: int) -> bool:
        """Delete a deal by its ID."""
        deal = self.deal_manager.filter(id=deal_id).first()
        if deal:
            deal.delete()
            return True
        return False
