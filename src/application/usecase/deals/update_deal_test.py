import unittest
from decimal import Decimal
from unittest.mock import Mock

from application.usecase.deals.update_deal import UpdateDealUseCase
from domain.deals.entity import DealEntity


class UpdateDealUseCaseTest(unittest.TestCase):
    def test_execute_updates_deal(self) -> None:
        mock_repo = Mock()
        expected_deal = DealEntity(
            id=1,
            title="Updated Deal",
            company_id=2,
            value=Decimal("200.0"),
            tags=[2, 3],
            distributor_id=4,
        )
        mock_repo.update.return_value = expected_deal
        usecase = UpdateDealUseCase(mock_repo)

        result = usecase.execute(
            deal_id=1,
            title="Updated Deal",
            distributor_id=4,
            tags=[2, 3],
            value=Decimal("200.0"),
        )
        self.assertEqual(result, expected_deal)
        mock_repo.update.assert_called_once_with(
            deal_id=1,
            title="Updated Deal",
            distributor_id=4,
            tags=[2, 3],
            value=Decimal("200.0"),
        )

    def test_execute_returns_none_if_not_found(self) -> None:
        mock_repo = Mock()
        mock_repo.update.return_value = None
        usecase = UpdateDealUseCase(mock_repo)

        result = usecase.execute(
            deal_id=99,
            title=None,
            distributor_id=None,
            tags=None,
            value=None,
        )
        self.assertIsNone(result)
        mock_repo.update.assert_called_once_with(
            deal_id=99,
            title=None,
            distributor_id=None,
            tags=None,
            value=None,
        )


if __name__ == "__main__":
    unittest.main()
