from decimal import Decimal

from domain.deals.entity import DealEntity
from domain.deals.repository import DealRepository


class UpdateDealUseCase:
    """Use case for updating an existing deal."""

    def __init__(self, repository: DealRepository) -> None:
        """Initialize with a DealRepository implementation."""
        self.repository = repository

    def execute(
        self,
        deal_id: int,
        title: str | None = None,
        distributor_id: int | None = None,
        tags: list[int] | None = None,
        value: Decimal | None = None,
    ) -> DealEntity | None:
        """Update an existing deal using the repository and return the updated entity.

        Returns None if the deal is not found.
        """
        return self.repository.update(
            deal_id=deal_id,
            title=title,
            distributor_id=distributor_id,
            tags=tags,
            value=value,
        )
