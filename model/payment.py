class Payment:
    PAYMENT_STATUS_PAID = "PAID"
    PAYMENT_STATUS_PENDING = "PENDING"

    def __init__(self, payment_type, amount, date_time, description, status=PAYMENT_STATUS_PENDING):
        if amount < 0:
            raise ValueError("Payment amount cannot be negative.")
        if not payment_type.strip():
            raise ValueError("Payment type cannot be empty.")
        self.payment_type = payment_type
        self.amount = amount
        self.date_time = date_time
        self.description = description
        self.status = status
        self.order = None

    def mark_as_paid(self):
        """Mark the payment as paid."""
        self.status = self.PAYMENT_STATUS_PAID

    def __repr__(self):
        return f"{self.__dict__}"