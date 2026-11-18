from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TransactionFactory:
    """Create validated transactions through a single construction point."""

    def create_transaction(self, amount, category: TransactionCategory):
        return Transaction(amount, category)
