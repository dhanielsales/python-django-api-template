import unittest
from decimal import Decimal

from .entity import DealEntity


class TestDealEntity(unittest.TestCase):
    """Unit tests for DealEntity."""

    def test_entity_creation(self) -> None:
        """Test creating a DealEntity with all fields."""
        entity = DealEntity(
            id=1,
            title="Test Deal",
            company_id=1,
            distributor_id=2,
            tags=[10, 20],
            value=Decimal(100.5),
        )
        self.assertEqual(entity.title, "Test Deal")
        self.assertEqual(entity.company_id, 1)
        self.assertEqual(entity.distributor_id, 2)
        self.assertEqual(entity.tags, [10, 20])
        self.assertEqual(entity.value, Decimal(100.5))

    def test_str(self) -> None:
        """Test the string representation of DealEntity."""
        entity = DealEntity(
            id=1,
            title="Test Deal",
            company_id=1,
            distributor_id=None,
            tags=None,
            value=None,
        )
        self.assertEqual(str(entity), "Test Deal (1)")

    def test_from_model(self) -> None:
        """Test creating a DealEntity from a model instance."""

        class DummyTag:
            def __init__(self, id: int) -> None:
                self.id = id

        class DummyDistributor:
            def __init__(self, id: int) -> None:
                self.id = id

        class DummyCompany:
            def __init__(self, id: int) -> None:
                self.id = id

        class DummyTags:
            def all(self) -> list[DummyTag]:
                return [DummyTag(1), DummyTag(2)]

        class DummyModel:
            id = 99
            title = "Deal Title"
            company = DummyCompany(1)
            distributor = DummyDistributor(5)
            tags = DummyTags()
            value = 200.0

        model = DummyModel()
        entity = DealEntity(
            id=model.id,
            title=model.title,
            company_id=model.company.id,
            distributor_id=model.distributor.id if model.distributor else None,
            tags=[tag.id for tag in model.tags.all()],
            value=Decimal(model.value),
        )
        self.assertEqual(entity.title, "Deal Title")
        self.assertEqual(entity.company_id, 1)
        self.assertEqual(entity.distributor_id, 5)
        self.assertEqual(entity.tags, [1, 2])
        self.assertEqual(entity.value, Decimal(200.0))


if __name__ == "__main__":
    unittest.main()
