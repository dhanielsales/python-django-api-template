import unittest
from decimal import Decimal
from unittest.mock import Mock

from application.usecase.deals.get_deal_by_id import GetDealByIdUseCase
from domain.deals.entity import DealEntity


class GetDealByIdUseCaseTest(unittest.TestCase):
    def test_execute_returns_deal(self) -> None:
        mock_repo = Mock()
        expected_deal = DealEntity(
            id=1,
            title="Deal",
            company_id=2,
            value=Decimal(100),
            tags=[],
            distributor_id=None,
        )
        mock_repo.get_one.return_value = expected_deal
        usecase = GetDealByIdUseCase(mock_repo)
        result = usecase.execute(1)
        self.assertEqual(result, expected_deal)
        mock_repo.get_one.assert_called_once_with(1)

    def test_execute_returns_none_if_not_found(self) -> None:
        mock_repo = Mock()
        mock_repo.get_one.return_value = None
        usecase = GetDealByIdUseCase(mock_repo)
        result = usecase.execute(99)
        self.assertIsNone(result)
        mock_repo.get_one.assert_called_once_with(99)


if __name__ == "__main__":
    unittest.main()
