"""This module serves as the entry point for the program."""
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver
from balance.balance_observer import PrintBalanceObserver
from finance_manager import FinanceManager
from transaction.transaction_category import TransactionCategory
from transaction.transaction_adapter import TransactionAdapter
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_factory import TransactionFactory


def main(balance=None, observers=None, transaction_factory=None):
    print("Adding transactions...")

    if balance is None:
        balance = Balance.get_instance()
    if observers is None:
        observers = [PrintBalanceObserver(), LowBalanceAlertObserver(threshold=100)]
    if transaction_factory is None:
        transaction_factory = TransactionFactory()
    manager = FinanceManager(balance, observers)

    transactions = [
        transaction_factory.create_transaction(100, TransactionCategory.INCOME),
        transaction_factory.create_transaction(50, TransactionCategory.EXPENSE),
        transaction_factory.create_transaction(200, TransactionCategory.INCOME),
        transaction_factory.create_transaction(75, TransactionCategory.EXPENSE),
    ]

    freelance_income = ExternalFreelanceIncome(1200, "INV-98765", "Mobile App Project")
    adapted_transaction = TransactionAdapter(freelance_income).to_transaction()
    all_transactions = transactions + [adapted_transaction]

    final_balance = manager.apply_transactions(all_transactions)
    print(balance.summary())
    return final_balance

if __name__ == "__main__":
    main()
