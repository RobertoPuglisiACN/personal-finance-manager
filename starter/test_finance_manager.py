import unittest

from finance_manager import FinanceManager
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class RecordingBalance:
    def __init__(self):
        self.observers = []
        self.transactions = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def apply_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_balance(self):
        return 42


class TestFinanceManager(unittest.TestCase):
    def test_uses_injected_balance_and_observers(self):
        balance = RecordingBalance()
        observer = object()
        manager = FinanceManager(balance, [observer])
        transaction = Transaction(30, TransactionCategory.INCOME)

        result = manager.apply_transactions([transaction])

        self.assertIs(manager.balance, balance)
        self.assertEqual(balance.observers, [observer])
        self.assertEqual(balance.transactions, [transaction])
        self.assertEqual(result, 42)


if __name__ == "__main__":
    unittest.main()
