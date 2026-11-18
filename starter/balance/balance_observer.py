# balance_observer.py

class IBalanceObserver:
    def update(self, balance, transaction):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class PrintBalanceObserver(IBalanceObserver):
    def update(self, balance, transaction):
        """Print balance update message."""
        print(f"Balance changed by {transaction}: ${balance:.2f}")


PrintObserver = PrintBalanceObserver


class LowBalanceAlertObserver(IBalanceObserver):
    def __init__(self, threshold):
        self.threshold = threshold
        self.alert_triggered = False

    def update(self, balance, transaction):
        """Alert if balance drops below threshold."""
        is_below_threshold = balance < self.threshold
        if is_below_threshold and not self.alert_triggered:
            print(
                f"Low balance alert: ${balance:.2f} is below "
                f"the ${self.threshold:.2f} threshold."
            )
        self.alert_triggered = is_below_threshold
