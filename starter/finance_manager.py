class FinanceManager:
    """Coordinate transactions using injected balance and observers."""

    def __init__(self, balance, observers=()):
        self.balance = balance
        self.observers = tuple(observers)
        for observer in self.observers:
            self.balance.register_observer(observer)

    def apply_transactions(self, transactions):
        for transaction in transactions:
            self.balance.apply_transaction(transaction)
        return self.balance.get_balance()
