import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintBalanceObserver
from contextlib import redirect_stdout
from io import StringIO

class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.observers = []

    def tearDown(self):
        for observer in self.observers:
            self.balance.unregister_observer(observer)

    def test_alert_triggers_on_low_balance(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.observers.append(observer)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        output = StringIO()
        with redirect_stdout(output):
            self.balance.apply_transaction(
                Transaction(60, TransactionCategory.EXPENSE)
            )
        self.assertTrue(observer.alert_triggered)
        self.assertIn("Low balance alert", output.getvalue())

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

    def test_print_observer_reports_changed_balance(self):
        observer = PrintBalanceObserver()
        self.observers.append(observer)
        self.balance.register_observer(observer)

        output = StringIO()
        with redirect_stdout(output):
            self.balance.apply_transaction(
                Transaction(25, TransactionCategory.INCOME)
            )

        self.assertIn("$25.00", output.getvalue())

if __name__ == "__main__":
    unittest.main()
