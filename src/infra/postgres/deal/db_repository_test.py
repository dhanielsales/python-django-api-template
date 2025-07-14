"""Unit tests for DealRepositoryDB."""

from decimal import Decimal
from unittest.mock import Mock, patch

import pytest
from src.django.models import (
    CompanyModel,
    DealModel,
    DistributorModel,
    TagModel,
)
from src.domain.deals.entity import DealEntity
from src.infra.postgres.deal.db_repository import DealRepositoryDB

from django.test import TestCase, TransactionTestCase


class TestDealRepositoryDB(TransactionTestCase):
    """Test cases for DealRepositoryDB."""

    def setUp(self) -> None:
        """Set up test data."""
        self.repository = DealRepositoryDB()

        # Create test company
        self.company = CompanyModel._default_manager.create(
            name="Test Company", address="123 Test St"
        )

        # Create test distributor
        self.distributor = DistributorModel._default_manager.create(
            name="Test Distributor", contact_email="distributor@test.com"
        )

        # Create test tags
        self.tag1 = TagModel._default_manager.create(name="Tag1")
        self.tag2 = TagModel._default_manager.create(name="Tag2")

    @patch("src.domain.deals.entity.DealEntity.from_model")
    def test_create_deal_success(self, mock_from_model: Mock) -> None:
        """Test successful deal creation."""
        # Arrange
        mock_entity = Mock(spec=DealEntity)
        mock_from_model.return_value = mock_entity

        title = "Test Deal"
        company_id = self.company.id
        distributor_id = self.distributor.id
        tags = [self.tag1.id, self.tag2.id]
        value = 1000.50

        # Act
        result = self.repository.create(
            title=title,
            company_id=company_id,
            distributor_id=distributor_id,
            tags=tags,
            value=value,
        )

        # Assert
        assert result == mock_entity
        mock_from_model.assert_called_once()

        # Verify deal was created in database
        deal = DealModel._default_manager.get(title=title)
        assert deal.title == title
        assert deal.company_id == company_id
        assert deal.distributor_id == distributor_id
        assert deal.value == Decimal(str(value))

    @patch("src.domain.deals.entity.DealEntity.from_model")
    def test_create_deal_without_optional_fields(self, mock_from_model: Mock) -> None:
        """Test deal creation without optional fields."""
        # Arrange
        mock_entity = Mock(spec=DealEntity)
        mock_from_model.return_value = mock_entity

        title = "Test Deal"
        company_id = self.company.id

        # Act
        result = self.repository.create(
            title=title, company_id=company_id, distributor_id=None, tags=None, value=None
        )

        # Assert
        assert result == mock_entity
        deal = DealModel._default_manager.get(title=title)
        assert deal.distributor_id is None
        assert deal.value is None

    @patch("src.domain.deals.entity.DealEntity.from_model")
    def test_get_one_existing_deal(self, mock_from_model: Mock) -> None:
        """Test retrieving an existing deal."""
        # Arrange
        deal = DealModel._default_manager.create(
            title="Test Deal", company=self.company, value=Decimal("100.00")
        )
        mock_entity = Mock(spec=DealEntity)
        mock_from_model.return_value = mock_entity

        # Act
        result = self.repository.get_one(deal.id)

        # Assert
        assert result == mock_entity
        mock_from_model.assert_called_once_with(deal)

    def test_get_one_nonexistent_deal(self) -> None:
        """Test retrieving a non-existent deal."""
        # Act
        result = self.repository.get_one(999)

        # Assert
        assert result is None

    @patch("src.domain.deals.entity.DealEntity.from_model")
    def test_get_all_deals(self, mock_from_model: Mock) -> None:
        """Test retrieving all deals."""
        # Arrange
        DealModel._default_manager.create(
            title="Deal 1", company=self.company, value=Decimal("100.00")
        )
        DealModel._default_manager.create(
            title="Deal 2", company=self.company, value=Decimal("200.00")
        )

        mock_entity1 = Mock(spec=DealEntity)
        mock_entity2 = Mock(spec=DealEntity)
        mock_from_model.side_effect = [mock_entity1, mock_entity2]

        # Act
        result = self.repository.get_all()

        # Assert
        assert len(result) == 2
        assert result == [mock_entity1, mock_entity2]
        assert mock_from_model.call_count == 2

    def test_get_all_no_deals(self) -> None:
        """Test retrieving all deals when none exist."""
        # Act
        result = self.repository.get_all()

        # Assert
        assert result == []

    @patch("src.domain.deals.entity.DealEntity.from_model")
    @patch("src.infrastructure.deals.repository_db.datetime")
    def test_update_deal_success(
        self, mock_datetime: Mock, mock_from_model: Mock
    ) -> None:
        """Test successful deal update."""
        # Arrange
        deal = DealModel._default_manager.create(
            title="Original Title", company=self.company, value=Decimal("100.00")
        )

        mock_now = Mock()
        mock_datetime.now.return_value = mock_now
        mock_entity = Mock(spec=DealEntity)
        mock_from_model.return_value = mock_entity

        new_title = "Updated Title"
        new_value = Decimal("200.00")

        # Act
        result = self.repository.update(
            deal_id=deal.id,
            title=new_title,
            distributor_id=self.distributor.id,
            tags=[self.tag1.id],
            value=new_value,
        )

        # Assert
        assert result == mock_entity

        # Verify database update
        updated_deal = DealModel._default_manager.get(id=deal.id)
        assert updated_deal.title == new_title
        assert updated_deal.value == new_value
        assert updated_deal.distributor_id == self.distributor.id

    def test_update_nonexistent_deal(self) -> None:
        """Test updating a non-existent deal."""
        # Act & Assert
        with pytest.raises(ValueError, match="Deal with ID 999 does not exist"):
            self.repository.update(
                deal_id=999, title="New Title", distributor_id=None, tags=None, value=None
            )

    def test_update_with_nonexistent_distributor(self) -> None:
        """Test updating deal with non-existent distributor."""
        # Arrange
        deal = DealModel._default_manager.create(
            title="Test Deal", company=self.company, value=Decimal("100.00")
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Distributor with ID 999 does not exist"):
            self.repository.update(
                deal_id=deal.id, title=None, distributor_id=999, tags=None, value=None
            )

    @patch("src.domain.deals.entity.DealEntity.from_model")
    def test_update_with_none_values_keeps_original(self, mock_from_model: Mock) -> None:
        """Test that None values in update keep original values."""
        # Arrange
        original_title = "Original Title"
        original_value = Decimal("100.00")

        deal = DealModel._default_manager.create(
            title=original_title, company=self.company, value=original_value
        )

        mock_entity = Mock(spec=DealEntity)
        mock_from_model.return_value = mock_entity

        # Act
        self.repository.update(
            deal_id=deal.id, title=None, distributor_id=None, tags=None, value=None
        )

        # Assert
        updated_deal = DealModel._default_manager.get(id=deal.id)
        assert updated_deal.title == original_title
        assert updated_deal.value == original_value

    def test_delete_existing_deal(self) -> None:
        """Test deleting an existing deal."""
        # Arrange
        deal = DealModel._default_manager.create(
            title="Test Deal", company=self.company, value=Decimal("100.00")
        )
        deal_id = deal.id

        # Act
        result = self.repository.delete(deal_id)

        # Assert
        assert result is True
        assert not DealModel._default_manager.filter(id=deal_id).exists()

    def test_delete_nonexistent_deal(self) -> None:
        """Test deleting a non-existent deal."""
        # Act
        result = self.repository.delete(999)

        # Assert
        assert result is False

    def test_transaction_rollback_on_update_error(self) -> None:
        """Test that transaction rolls back on update error."""
        # Arrange
        deal = DealModel._default_manager.create(
            title="Test Deal", company=self.company, value=Decimal("100.00")
        )

        # Act & Assert
        with pytest.raises(ValueError):
            self.repository.update(
                deal_id=deal.id,
                title="New Title",
                distributor_id=999,  # Non-existent distributor
                tags=None,
                value=None,
            )

        # Verify original deal is unchanged
        unchanged_deal = DealModel._default_manager.get(id=deal.id)
        assert unchanged_deal.title == "Test Deal"


class TestDealRepositoryDBIntegration(TestCase):
    """Integration tests for DealRepositoryDB."""

    def setup(self) -> None:
        """Set up test data."""
        self.repository = DealRepositoryDB()
        self.company = CompanyModel._default_manager.create(
            name="Integration Test Company", address="456 Integration St"
        )

    def test_full_crud_cycle(self) -> None:
        """Test complete CRUD cycle."""
        # Create
        with patch("src.domain.deals.entity.DealEntity.from_model") as mock_from_model:
            mock_entity = Mock(spec=DealEntity)
            mock_from_model.return_value = mock_entity

            created_deal = self.repository.create(
                title="CRUD Test Deal",
                company_id=self.company.id,
                distributor_id=None,
                tags=None,
                value=500.00,
            )

            assert created_deal == mock_entity

        # Get the actual deal from database for further testing
        deal = DealModel._default_manager.get(title="CRUD Test Deal")

        # Read
        with patch("src.domain.deals.entity.DealEntity.from_model") as mock_from_model:
            mock_entity = Mock(spec=DealEntity)
            mock_from_model.return_value = mock_entity

            retrieved_deal = self.repository.get_one(deal.id)
            assert retrieved_deal == mock_entity

        # Update
        with patch("src.domain.deals.entity.DealEntity.from_model") as mock_from_model:
            mock_entity = Mock(spec=DealEntity)
            mock_from_model.return_value = mock_entity

            updated_deal = self.repository.update(
                deal_id=deal.id,
                title="Updated CRUD Deal",
                distributor_id=None,
                tags=None,
                value=Decimal("750.00"),
            )
            assert updated_deal == mock_entity

        # Verify update
        updated_deal_db = DealModel._default_manager.get(id=deal.id)
        assert updated_deal_db.title == "Updated CRUD Deal"
        assert updated_deal_db.value == Decimal("750.00")

        # Delete
        delete_result = self.repository.delete(deal.id)
        assert delete_result is True
        assert not DealModel._default_manager.filter(id=deal.id).exists()
