from domain.deals.entity import DealEntity
from domain.deals.repository import DealRepository


class GetDealByIdUseCase:
    """Use case for retrieving a deal by its ID."""

    def __init__(self, repository: DealRepository) -> None:
        """Initialize with a DealRepository implementation."""
        self.repository = repository

    def execute(self, deal_id: int) -> DealEntity | None:
        """Retrieve a deal by its ID. Returns None if not found."""
        return self.repository.get_one(deal_id)
