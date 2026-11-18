# Personal Finance Manager

A small, dependency-free Python application for recording income and expenses,
tracking the current balance, and reporting low-balance alerts.

Run the application from this directory:

```powershell
python main.py
```

Run the unit tests:

```powershell
python -m unittest discover -v
```

## Design patterns

- **Singleton — `balance.balance.Balance`:** `Balance()` and
  `Balance.get_instance()` return the same balance manager. This is appropriate
  for the app's single shared balance: every income and expense updates the same
  source of truth rather than separate, inconsistent copies.
- **Adapter — `transaction.transaction_adapter.TransactionAdapter`:** converts
  third-party freelance income into the application's standard income
  `Transaction`. It isolates the core model from the external provider's
  transaction shape, so provider-specific details do not leak into balance
  processing.
- **Observer — `balance.balance_observer`:** the balance notifies registered
  observers after each transaction. `PrintBalanceObserver` reports the new
  balance, and `LowBalanceAlertObserver` alerts when the balance falls below
  its configured threshold. This is appropriate because balance updates can
  trigger independent responses without making the balance manager depend on
  console output or alert behavior.
- **Factory — `transaction.transaction_factory.TransactionFactory`:** creates
  standard `Transaction` objects through `create_transaction`. This pattern
  was chosen as the additional pattern because it separates object construction
  from the sample workflow while remaining small and useful for the current
  application.

### Why Factory, where it fits, and its benefits

`TransactionFactory` is used by `main()` to create each standard income or
expense transaction. The freelance transaction follows a different path through
`TransactionAdapter`, which translates the external object into the same
application model.

Keeping standard transaction construction in one place makes it easier to
change or extend creation rules (for example, adding validation or new
transaction variants) without spreading that logic across the application.

- **Flexibility:** creation rules can change independently of the workflow that
  applies transactions.
- **Testability:** tests can inject a substitute factory, separating
  orchestration tests from transaction construction.
- **Scalability:** as more transaction categories or sources are introduced,
  their standard object construction can be added in one focused place.

- **Dependency injection:** `FinanceManager` receives its balance and observers
  in its constructor. `main()` supplies defaults but also accepts injected
  dependencies, allowing callers and tests to substitute them without a
  framework.

The project is organized into `balance/` and `transaction/` modules, with
`finance_manager.py` coordinating the application and `main.py` demonstrating
the complete workflow.
