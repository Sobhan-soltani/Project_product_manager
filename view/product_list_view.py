# view/product_list_view.py
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QListWidget, QLineEdit, QPushButton, QMessageBox,
                               QDateEdit, QSpinBox, QComboBox, QListWidgetItem)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import QDate, Qt, QSize
from repository.product_repository import ProductRepository
from service.product_service import ProductService

class ProductListView(QMainWindow):
    def __init__(self, user_id, user_repository, panel_view):
        super().__init__()
        self.user_id = user_id
        self.product_repository = ProductRepository(user_repository.conn)
        self.product_service = ProductService(self.product_repository)
        self.panel_view = panel_view
        self.setWindowTitle("Product List")
        self.setGeometry(100, 100, 800, 500)  # Increased window size

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Product List Display
        self.product_list = QListWidget()
        self.product_list.setFont(QFont("Courier New", 10))
        self.product_list.setStyleSheet("""
            QListWidget {
                background-color: #f5f5f5;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                border-bottom: 1px solid #cccccc;
                padding: 8px;
                background-color: white;
                margin: 2px;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #e0f0ff;
                border: 1px solid #a0a0a0;
            }
        """)
        self.product_list.setMinimumWidth(500)
        self.product_list.itemClicked.connect(self.load_products)
        self.layout.addWidget(self.product_list)

        # Add header
        self.add_list_header()
        # Add header
        header_item = QListWidgetItem("Name".ljust(15) + "Company".ljust(15) + "Price".ljust(10) + "Quantity")
        header_item.setFlags(header_item.flags() & ~Qt.ItemIsSelectable)  # Make header non-selectable
        self.product_list.addItem(header_item)

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

    def add_list_header(self):
        # Header widget with custom styling
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            background-color: #e0e0e0;
            border-radius: 3px;
            padding: 5px;
        """)
        header_layout = QHBoxLayout(header_widget)

        labels = ["Name", "Company", "Price", "Quantity"]
        widths = [150, 150, 100, 80]  # Adjusted widths

        for label, width in zip(labels, widths):
            lbl = QLineEdit(label)
            lbl.setReadOnly(True)
            lbl.setStyleSheet("""
                QLineEdit {
                    border: none;
                    background: transparent;
                    font-weight: bold;
                    font-size: 12px;
                }
            """)
            lbl.setMinimumWidth(width)
            header_layout.addWidget(lbl)

        header_item = QListWidgetItem()
        header_item.setSizeHint(header_widget.sizeHint())
        header_item.setFlags(Qt.NoItemFlags)
        self.product_list.addItem(header_item)
        self.product_list.setItemWidget(header_item, header_widget)

    def load_products(self):
        self.product_list.clear()
        self.add_list_header()  # Add header first

        products = self.product_service.get_user_products(self.user_id)
        for product in products:
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(5, 5, 5, 5)

            # Create styled fields
            fields = [
                (product.name, 150),
                (product.company_name, 150),
                (f"${product.price:.2f}", 100),
                (str(product.quantity), 80)
            ]

            for text, width in fields:
                lbl = QLineEdit(text)
                lbl.setReadOnly(True)
                lbl.setStyleSheet("""
                    QLineEdit {
                        border: none;
                        background: transparent;
                        font-size: 12px;
                    }
                """)
                lbl.setMinimumWidth(width)
                item_layout.addWidget(lbl)

            # Create list item
            list_item = QListWidgetItem()
            list_item.setSizeHint(QSize(0, 40))  # Fixed height
            self.product_list.addItem(list_item)
            self.product_list.setItemWidget(list_item, item_widget)

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