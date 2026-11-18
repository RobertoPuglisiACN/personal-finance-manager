# balance.py

from threading import Lock, RLock

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class Balance:
    """Singleton to track the balance."""

    _instance = None
    _instance_lock = Lock()
    _initialization_lock = Lock()

    def __init__(self):
        """Initialize the shared balance once."""
        with self._initialization_lock:
            if getattr(self, "_initialized", False):
                return

            self._balance = 0.0
            self._observers = []
            self._lock = RLock()
            self._initialized = True

    def __new__(cls):
        """Return the single shared balance manager."""
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    @classmethod
    def get_instance(cls):
        """Return the shared balance manager."""
        return cls()

    def register_observer(self, observer):
        """Subscribe an observer to balance changes."""
        if not callable(getattr(observer, "update", None)):
            raise TypeError("Observer must provide an update method.")
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)

    def unregister_observer(self, observer):
        """Remove an observer from balance change notifications."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)

    def reset(self):
        """Reset the net balance to zero."""
        with self._lock:
            self._balance = 0.0

    def add_income(self, amount):
        """Add income to the balance."""
        self.apply_transaction(Transaction(amount, TransactionCategory.INCOME))

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self.apply_transaction(Transaction(amount, TransactionCategory.EXPENSE))

    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance.

        Args:
            transaction (Transaction): The transaction to apply.
        """
        if not isinstance(transaction, Transaction):
            raise TypeError("transaction must be a Transaction instance.")

        with self._lock:
            if transaction.category == TransactionCategory.INCOME:
                self._balance += transaction.amount
            elif transaction.category == TransactionCategory.EXPENSE:
                self._balance -= transaction.amount
            else:
                raise ValueError("Unsupported transaction category.")

            balance = self._balance
            observers = tuple(self._observers)

        for observer in observers:
            observer.update(balance, transaction)

    def get_balance(self):
        """Get the current net balance."""
        with self._lock:
            return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Current balance: ${self.get_balance():.2f}"
