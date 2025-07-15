import unittest
from unittest.mock import Mock

from application.usecase.deals.delete_deal import DeleteDealUseCase


class DeleteDealUseCaseTest(unittest.TestCase):
    def test_execute_deletes_deal(self) -> None:
        mock_repo = Mock()
        mock_repo.delete.return_value = True
        usecase = DeleteDealUseCase(mock_repo)
        result = usecase.execute(1)
        self.assertTrue(result)
        mock_repo.delete.assert_called_once_with(1)

    def test_execute_returns_false_if_not_found(self) -> None:
        mock_repo = Mock()
        mock_repo.delete.return_value = False
        usecase = DeleteDealUseCase(mock_repo)
        result = usecase.execute(99)
        self.assertFalse(result)
        mock_repo.delete.assert_called_once_with(99)


if __name__ == "__main__":
    unittest.main()
