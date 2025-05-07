# view/panel_view.py
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton)
from view.product_list_view import ProductListView
from view.order_view import OrderView
from view.payment_view import PaymentView

class PanelView(QMainWindow):
    def __init__(self, user, user_repository, product_service, order_service):
        super().__init__()
        self.user = user
        self.user_repository = user_repository
        self.product_service = product_service
        self.order_service = order_service
        self.setWindowTitle("User Panel")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.product_list_button = QPushButton("Product List")
        self.product_list_button.clicked.connect(self.show_product_list)
        self.layout.addWidget(self.product_list_button)

        self.order_button = QPushButton("Order")
        self.order_button.clicked.connect(self.show_order)
        self.layout.addWidget(self.order_button)

        self.payment_button = QPushButton("Payment")
        self.payment_button.clicked.connect(self.show_payment)
        self.layout.addWidget(self.payment_button)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button)

    def show_product_list(self):
        self.product_list_view = ProductListView(self.user.id, self.user_repository, self)
        self.product_list_view.show()
        self.hide()

    def show_order(self):
        self.order_view = OrderView(self.user, self.order_service, self.product_service, self)
        self.order_view.show()
        self.hide()

    def show_payment(self):
        self.payment_view = PaymentView(self.user, self.order_service, self)
        self.payment_view.show()
        self.hide()

    def logout(self):
        self.close()