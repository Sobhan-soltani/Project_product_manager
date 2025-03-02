# view/product_list_view.py
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QListWidget, QLineEdit, QPushButton, QMessageBox, QDateEdit, QSpinBox, QComboBox)
from PySide6.QtCore import QDate
from repository.product_repository import ProductRepository
from service.product_service import ProductService

class ProductListView(QMainWindow):
    def __init__(self, user_id, user_repository, panel_view):
        super().__init__()
        self.user_id = user_id
        self.product_repository = ProductRepository(user_repository.conn)
        self.product_service = ProductService(self.product_repository)
        self.panel_view = panel_view  # Reference to previous page
        self.setWindowTitle("Product List")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Product List Display
        self.product_list = QListWidget()
        self.product_list.itemClicked.connect(self.load_product_details)
        self.layout.addWidget(self.product_list)

        # Form for Adding/Editing Products
        self.form_layout = QVBoxLayout()

        self.category_input = QComboBox()
        self.category_input.addItems(["Electronics", "Clothing", "Food", "Other"])
        self.form_layout.addWidget(self.category_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Product Name")
        self.form_layout.addWidget(self.name_input)

        self.company_name_input = QLineEdit()
        self.company_name_input.setPlaceholderText("Company Name")
        self.form_layout.addWidget(self.company_name_input)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price")
        self.form_layout.addWidget(self.price_input)

        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 10000)
        self.form_layout.addWidget(self.quantity_input)

        self.exp_date_input = QDateEdit()
        self.exp_date_input.setCalendarPopup(True)
        self.exp_date_input.setDate(QDate.currentDate())
        self.form_layout.addWidget(self.exp_date_input)

        self.add_button = QPushButton("Add Product")
        self.add_button.clicked.connect(self.add_product)
        self.form_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Product")
        self.edit_button.clicked.connect(self.edit_product)
        self.form_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Product")
        self.delete_button.clicked.connect(self.delete_product)
        self.form_layout.addWidget(self.delete_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.form_layout.addWidget(self.back_button)

        self.layout.addLayout(self.form_layout)
        self.load_products()

    def load_products(self):
        self.product_list.clear()
        products = self.product_service.get_user_products(self.user_id)
        for product in products:
            self.product_list.addItem(f"{product.name} - {product.company_name} - {product.price} - Qty: {product.quantity}")

    def load_product_details(self, item):
        product_name = item.text().split(" - ")[0]
        products = self.product_service.get_user_products(self.user_id)
        product = next((p for p in products if p.name == product_name), None)
        if product:
            self.category_input.setCurrentText(product.category)
            self.name_input.setText(product.name)
            self.company_name_input.setText(product.company_name)
            self.price_input.setText(str(product.price))
            self.quantity_input.setValue(product.quantity)
            self.exp_date_input.setDate(QDate.fromString(product.exp_date, "yyyy-MM-dd"))

    def add_product(self):
        category = self.category_input.currentText()
        name = self.name_input.text()
        company_name = self.company_name_input.text()
        price = self.price_input.text()
        quantity = self.quantity_input.value()
        exp_date = self.exp_date_input.date().toString("yyyy-MM-dd")

        if not category or not name or not company_name or not price or quantity <= 0:
            QMessageBox.warning(self, "Error", "All fields except expiration date are required")
            return

        try:
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, "Error", "Price must be a number")
            return

        self.product_service.add_product(category, name, company_name, price, quantity, exp_date, self.user_id)
        self.load_products()
        self.clear_form()

    def edit_product(self):
        selected_item = self.product_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "Select a product to edit")
            return
        product_name = selected_item.text().split(" - ")[0]
        products = self.product_service.get_user_products(self.user_id)
        product = next((p for p in products if p.name == product_name), None)
        if product:
            category = self.category_input.currentText()
            name = self.name_input.text()
            company_name = self.company_name_input.text()
            price = self.price_input.text()
            quantity = self.quantity_input.value()
            exp_date = self.exp_date_input.date().toString("yyyy-MM-dd")

            if not category or not name or not company_name or not price or quantity <= 0:
                QMessageBox.warning(self, "Error", "All fields except expiration date are required")
                return

            try:
                price = float(price)
            except ValueError:
                QMessageBox.warning(self, "Error", "Price must be a number")
                return

            self.product_service.update_product(product.id, category, name, company_name, price, quantity, exp_date)
            self.load_products()
            self.clear_form()

    def delete_product(self):
        selected_item = self.product_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "Select a product to delete")
            return
        product_name = selected_item.text().split(" - ")[0]
        products = self.product_service.get_user_products(self.user_id)
        product = next((p for p in products if p.name == product_name), None)
        if product:
            self.product_service.delete_product(product.id)
            self.load_products()
            self.clear_form()

    def clear_form(self):
        self.category_input.setCurrentIndex(0)
        self.name_input.clear()
        self.company_name_input.clear()
        self.price_input.clear()
        self.quantity_input.setValue(0)
        self.exp_date_input.setDate(QDate.currentDate())

    def go_back(self):
        self.panel_view.show()
        self.close()