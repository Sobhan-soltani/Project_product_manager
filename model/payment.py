class Payment:
    def __init__(self, payment_type, amount, date_time, description):
        self.payment_type = payment_type
        self.amount = amount
        self.date_time = date_time
        self.description = description
        self.order = None
