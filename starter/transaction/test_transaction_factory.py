import unittest

from transaction.transaction_category import TransactionCategory
from transaction.transaction_factory import TransactionFactory
from transaction.transaction import Transaction


class TestTransactionFactory(unittest.TestCase):
    def test_factory_creates_transaction(self):
        transaction = TransactionFactory().create_transaction(
            75, TransactionCategory.EXPENSE
        )

        self.assertEqual(transaction, Transaction(75, TransactionCategory.EXPENSE))


if __name__ == "__main__":
    unittest.main()
