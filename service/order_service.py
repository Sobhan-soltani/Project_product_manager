# service/order_service.py
from datetime import datetime
from model.order import Order
from model.order_item import OrderItem
from model.payment import Payment

class OrderService:
    def __init__(self, order_repository, product_service):
        self.order_repository = order_repository
        self.product_service = product_service

    def create_order(self, user, product_id, quantity):
        product, total_cost = self.product_service.purchase_product(product_id, quantity)
        order = Order(None, user, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        order_item = OrderItem(None, product, quantity, product.price)
        order.add_item(order_item)
        order_id = self.order_repository.save_order(order)
        return order, total_cost

    def add_payment(self, order, payment_type, amount, description):
        payment = Payment(payment_type, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description)
        payment.mark_as_paid()
        success, message = self.order_repository.add_payment_to_order(order, payment)
        if not success:
            raise ValueError(message)
        return payment

    def get_user_orders(self, user_id):
        return []