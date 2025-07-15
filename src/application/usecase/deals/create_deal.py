from decimal import Decimal

from domain.deals.entity import DealEntity
from domain.deals.repository import DealRepository


class CreateDealUseCase:
    """Use case for creating a new deal."""

    def __init__(self, repository: DealRepository) -> None:
        """Initialize with a DealRepository implementation."""
        self.repository = repository

    def execute(
        self,
        title: str,
        company_id: int,
        value: Decimal,
        tags: list[int] | None = None,
        distributor_id: int | None = None,
    ) -> DealEntity:
        """Create a new deal using the repository and return the created entity."""
        return self.repository.create(
            title=title,
            company_id=company_id,
            value=value,
            tags=tags,
            distributor_id=distributor_id,
        )
