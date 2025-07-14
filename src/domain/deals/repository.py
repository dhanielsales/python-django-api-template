from decimal import Decimal
from typing import Protocol

from src.domain.deals.entity import DealEntity


class DealRepository(Protocol):
    """Protocol defining the interface for deal repository implementations."""

    def create(
        self,
        title: str,
        company_id: int,
        distributor_id: int | None,
        tags: list[int] | None,
        value: float | None,
    ) -> DealEntity:
        """Create a new deal.

        Args:
            title: The title of the deal
            company_id: ID of the associated company
            distributor_id: Optional ID of the associated distributor
            tags: Optional list of tag IDs to associate with the deal
            value: Optional value of the deal

        Returns:
            DealEntity: The created deal entity
        """
        ...

    def get_one(self, deal_id: int) -> DealEntity | None:
        """Retrieve a deal by its ID.

        Args:
            deal_id: The ID of the deal to retrieve

        Returns:
            DealEntity | None: The deal entity if found, None otherwise
        """
        ...

    def get_all(self) -> list[DealEntity]:
        """Retrieve all deals.

        Returns:
            list[DealEntity]: List of all deal entities
        """
        ...

    def update(
        self,
        deal_id: int,
        title: str | None,
        distributor_id: int | None,
        tags: list[int] | None,
        value: Decimal | None,
    ) -> DealEntity | None:
        """Update an existing deal.

        Args:
            deal_id: ID of the deal to update
            title: Optional new title for the deal
            distributor_id: Optional new distributor ID
            tags: Optional new list of tag IDs
            value: Optional new value for the deal

        Returns:
            DealEntity | None: The updated deal entity if successful, None otherwise

        Raises:
            ValueError: If the deal or distributor doesn't exist
        """
        ...

    def delete(self, deal_id: int) -> bool:
        """Delete a deal by its ID.

        Args:
            deal_id: The ID of the deal to delete

        Returns:
            bool: True if the deal was deleted successfully, False otherwise
        """
        ...
