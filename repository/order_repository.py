# repository/order_repository.py
from datetime import datetime
from model.order import Order
from model.payment import Payment
from model.order_item import OrderItem

class OrderRepository:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def save_order(self, order):
        # Save the order
        self.cursor.execute('''
            INSERT INTO orders (user_id, date_time, total_cost)
            VALUES (?, ?, ?)
        ''', (order.user.id, order.date_time, order.total_cost))
        self.conn.commit()
        order.id = self.cursor.lastrowid

        # Save order items
        for item in order.order_item_list:
            self.cursor.execute('''
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order.id, item.product.product_id, item.quantity, item.price))
            self.conn.commit()
            item.id = self.cursor.lastrowid
            item.order = order

        # Save payments
        for payment in order.payment_list:
            self.cursor.execute('''
                INSERT INTO payments (order_id, payment_type, amount, date_time, description, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (order.id, payment.payment_type, payment.amount, payment.date_time, payment.description, payment.status))
            self.conn.commit()
            payment.order = order

        return order.id

    def check_payment_status(self, payment):
        return payment.status == Payment.PAYMENT_STATUS_PAID

    def add_payment_to_order(self, order, payment):
        if not self.check_payment_status(payment):
            return False, "Payment failed: Status is not PAID"

        payment.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order.add_payment(payment)
        self.cursor.execute('''
            INSERT INTO payments (order_id, payment_type, amount, date_time, description, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (order.id, payment.payment_type, payment.amount, payment.date_time, payment.description, payment.status))
        self.conn.commit()
        return True, "Payment added successfully"