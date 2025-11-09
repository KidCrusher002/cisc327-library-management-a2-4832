"""
Mockable Payment Service
Simulates external payment processing (for testing with mocks/stubs).
"""

import random
import string
import time

class PaymentGateway:
    """A mockable external payment gateway class."""

    def process_payment(self, patron_id: str, amount: float) -> dict:
        """
        Simulates sending a payment request to an external service.
        In a real system, this would call an API.
        """
        # Simulate network latency
        time.sleep(0.1)

        # Fake success or failure randomly for realism
        if amount <= 0:
            return {"status": "failed", "error": "Invalid amount"}

        if random.random() < 0.9:
            transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            return {"status": "success", "transaction_id": transaction_id}
        else:
            return {"status": "failed", "error": "Network error"}

    def refund_payment(self, transaction_id: str, amount: float) -> dict:
        """Simulates refund processing."""
        time.sleep(0.1)

        if not transaction_id:
            return {"status": "failed", "error": "Missing transaction ID"}

        if amount <= 0:
            return {"status": "failed", "error": "Invalid refund amount"}

        refund_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return {"status": "success", "refund_id": refund_id}
