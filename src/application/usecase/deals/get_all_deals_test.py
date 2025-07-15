import unittest
from decimal import Decimal
from unittest.mock import Mock

from application.usecase.deals.get_all_deals import GetAllDealsUseCase
from domain.deals.entity import DealEntity


class GetAllDealsUseCaseTest(unittest.TestCase):
    def test_execute_returns_all_deals(self) -> None:
        mock_repo = Mock()
        deals = [
            DealEntity(
                id=1,
                title="Deal1",
                company_id=2,
                value=Decimal(100),
                tags=[],
                distributor_id=None,
            ),
            DealEntity(
                id=2,
                title="Deal2",
                company_id=3,
                value=Decimal(200),
                tags=[1],
                distributor_id=4,
            ),
        ]
        mock_repo.get_all.return_value = deals
        usecase = GetAllDealsUseCase(mock_repo)
        result = usecase.execute()
        self.assertEqual(result, deals)
        mock_repo.get_all.assert_called_once_with()

    def test_execute_returns_empty_list(self) -> None:
        mock_repo = Mock()
        mock_repo.get_all.return_value = []
        usecase = GetAllDealsUseCase(mock_repo)
        result = usecase.execute()
        self.assertEqual(result, [])
        mock_repo.get_all.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
