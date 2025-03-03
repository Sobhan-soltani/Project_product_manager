class OrderItem:
    def __init__(self, id, product, quantity, price):
        self.id = id
        self.order = None
        self.product = product
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"{self.__dict__}"