from domain.deals.entity import DealEntity
from domain.deals.repository import DealRepository


class GetAllDealsUseCase:
    """Use case for retrieving all deals."""

    def __init__(self, repository: DealRepository) -> None:
        """Initialize with a DealRepository implementation."""
        self.repository = repository

    def execute(self) -> list[DealEntity]:
        """Retrieve all deals."""
        return self.repository.get_all()
