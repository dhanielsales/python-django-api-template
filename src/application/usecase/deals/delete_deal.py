from domain.deals.repository import DealRepository


class DeleteDealUseCase:
    """Use case for deleting a deal by its ID."""

    def __init__(self, repository: DealRepository) -> None:
        """Initialize with a DealRepository implementation."""
        self.repository = repository

    def execute(self, deal_id: int) -> bool:
        """Delete a deal by its ID. Returns True if deleted, False otherwise."""
        return self.repository.delete(deal_id)
