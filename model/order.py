class Order:
    def __init__(self, id, user, date_time, order_item_list = None, payment_list= None):
        self.id = id
        self.user = user
        self.date_time = date_time
        self.order_item_list = order_item_list if order_item_list else []
        self.total_cost = 0
        self.payment_list = payment_list if payment_list else []


    def add_item(self, *items):
        for item in items:
            self.total_cost += item.price * item.quantity
            self.order_item_list.append(item)

    def add_payment(self, *payments):
        for payment in payments:
            self.payment_list.append(payment)


    def __repr__(self):
        return f"{self.__dict__}"