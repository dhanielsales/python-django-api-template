import unittest
from decimal import Decimal
from unittest.mock import Mock

from application.usecase.deals.create_deal import CreateDealUseCase
from domain.deals.entity import DealEntity


class CreateDealUseCaseTest(unittest.TestCase):
    def test_execute_creates_deal(self) -> None:
        mock_repo = Mock()
        expected_deal = DealEntity(
            id=1,
            title="Test Deal",
            company_id=2,
            value=Decimal("100.0"),
            tags=[1, 2],
            distributor_id=3,
        )
        mock_repo.create.return_value = expected_deal
        usecase = CreateDealUseCase(mock_repo)

        result = usecase.execute(
            title="Test Deal",
            company_id=2,
            value=Decimal("100.0"),
            tags=[1, 2],
            distributor_id=3,
        )
        self.assertEqual(result, expected_deal)
        mock_repo.create.assert_called_once_with(
            title="Test Deal",
            company_id=2,
            value=Decimal("100.0"),
            tags=[1, 2],
            distributor_id=3,
        )


if __name__ == "__main__":
    unittest.main()
