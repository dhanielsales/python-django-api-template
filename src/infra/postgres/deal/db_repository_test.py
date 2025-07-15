from decimal import Decimal

from django.test import TestCase

from core.models import DistributorModel, TagModel
from infra.postgres.deal.db_repository import DealRepositoryDB


class DealRepositoryDBIntegrationTest(TestCase):
    def setUp(self) -> None:
        from core.models import CompanyModel

        self.repo = DealRepositoryDB()
        self.company = CompanyModel.objects.create(name="Test Company")
        self.distributor = DistributorModel.objects.create(name="D1")
        self.tag1 = TagModel.objects.create(name="tag1")
        self.tag2 = TagModel.objects.create(name="tag2")

    def test_create_and_get(self) -> None:
        deal_entity = self.repo.create(
            title="Test Deal",
            company_id=self.company.id,
            value=Decimal("100.0"),
            tags=[self.tag1.id, self.tag2.id],
            distributor_id=self.distributor.id,
        )
        self.assertEqual(deal_entity.title, "Test Deal")
        self.assertEqual(deal_entity.distributor_id, self.distributor.id)

        assert deal_entity.tags is not None
        self.assertIn(self.tag1.id, deal_entity.tags)
        self.assertIn(self.tag2.id, deal_entity.tags)

        # Test get_one
        found = self.repo.get_one(deal_entity.id)
        self.assertIsNotNone(found)
        assert found is not None
        self.assertEqual(found.title, "Test Deal")

    def test_update(self) -> None:
        deal_entity = self.repo.create(
            title="To Update",
            company_id=self.company.id,
            value=Decimal("50.0"),
            tags=[self.tag1.id],
            distributor_id=self.distributor.id,
        )
        updated = self.repo.update(
            deal_id=deal_entity.id,
            title="Updated Title",
            distributor_id=self.distributor.id,
            tags=[self.tag2.id],
            value=Decimal("200.0"),
        )
        assert updated is not None
        self.assertEqual(updated.title, "Updated Title")
        self.assertEqual(updated.value, Decimal("200.0"))

        assert updated.tags is not None
        self.assertIn(self.tag2.id, updated.tags)

    def test_delete(self) -> None:
        deal_entity = self.repo.create(
            title="To Delete",
            company_id=self.company.id,
            value=Decimal("10.0"),
            tags=[self.tag1.id],
            distributor_id=self.distributor.id,
        )
        deleted = self.repo.delete(deal_entity.id)
        self.assertTrue(deleted)
        self.assertIsNone(self.repo.get_one(deal_entity.id))

    def test_get_one_not_found(self) -> None:
        self.assertIsNone(self.repo.get_one(9999))

    def test_delete_not_found(self) -> None:
        self.assertFalse(self.repo.delete(9999))
