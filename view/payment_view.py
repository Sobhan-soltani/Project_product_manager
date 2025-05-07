# view/payment_view.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QComboBox, QTextEdit
from model.order import Order

class PaymentView(QDialog):
    def __init__(self, user, order_service, panel_view, order=None):
        super().__init__()
        self.user = user
        self.order_service = order_service
        self.panel_view = panel_view
        self.order = order  # The order to pay for (optional)
        self.setWindowTitle("Payment")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.order_id_input = QLineEdit()
        self.order_id_input.setPlaceholderText("Order ID")
        self.layout.addWidget(self.order_id_input)

        self.payment_type_input = QComboBox()
        self.payment_type_input.addItems(["Credit Card", "PayPal", "Cash"])
        self.layout.addWidget(self.payment_type_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        self.layout.addWidget(self.amount_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description")
        self.layout.addWidget(self.description_input)

        self.pay_button = QPushButton("Make Payment")
        self.pay_button.clicked.connect(self.make_payment)
        self.layout.addWidget(self.pay_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

        # If an order is provided, prefill the order ID and amount
        if self.order:
            self.order_id_input.setText(str(self.order.id))
            self.order_id_input.setReadOnly(True)
            self.amount_input.setText(str(self.order.total_cost))
            self.amount_input.setReadOnly(True)

    def make_payment(self):
        order_id = self.order_id_input.text()
        payment_type = self.payment_type_input.currentText()
        amount = self.amount_input.text()
        description = self.description_input.toPlainText()

        if not order_id or not amount:
            QMessageBox.warning(self, "Error", "Order ID and Amount are required")
            return

        try:
            order_id = int(order_id)
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, "Error", "Order ID and Amount must be numeric")
            return

        # Find the order (if not provided)
        if not self.order:
            orders = self.order_service.get_user_orders(self.user.id)
            self.order = next((o for o in orders if o.id == order_id), None)
            if not self.order:
                QMessageBox.warning(self, "Error", f"Order with ID {order_id} not found")
                return

        try:
            payment = self.order_service.add_payment(self.order, payment_type, amount, description)
            QMessageBox.information(self, "Success", "Payment recorded successfully")
            self.close()
            self.panel_view.show()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def go_back(self):
        self.panel_view.show()
        self.close()