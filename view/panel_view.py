# view/panel_view.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from view.product_list_view import ProductListView

class PanelView(QMainWindow):
    def __init__(self, user_id, user_repository, login_signup_view):
        super().__init__()
        self.user_id = user_id
        self.user_repository = user_repository
        self.login_signup_view = login_signup_view  # Reference to previous page
        self.setWindowTitle("User Panel")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.product_list_button = QPushButton("Product List")
        self.product_list_button.clicked.connect(self.open_product_list)
        self.layout.addWidget(self.product_list_button)

        self.storage_button = QPushButton("Storage")
        self.storage_button.clicked.connect(self.open_storage)
        self.layout.addWidget(self.storage_button)

        self.order_button = QPushButton("Order")
        self.order_button.clicked.connect(self.open_order)
        self.layout.addWidget(self.order_button)

        self.payment_button = QPushButton("Payment")
        self.payment_button.clicked.connect(self.open_payment)
        self.layout.addWidget(self.payment_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

    def open_product_list(self):
        self.product_list_view = ProductListView(self.user_id, self.user_repository, self)
        self.product_list_view.show()
        self.hide()

    def open_storage(self):
        print("Storage page not implemented yet")

    def open_order(self):
        print("Order page not implemented yet")

    def open_payment(self):
        print("Payment page not implemented yet")

    def go_back(self):
        self.login_signup_view.show()
        self.close()