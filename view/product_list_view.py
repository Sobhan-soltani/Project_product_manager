from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QListWidget, QLineEdit, QPushButton, QMessageBox,
                               QDateEdit, QSpinBox, QComboBox, QListWidgetItem, QLabel)
from PySide6.QtGui import QFont
from PySide6.QtCore import QDate, Qt, QSize
from repository.product_repository import ProductRepository
from service.product_service import ProductService

class ProductListView(QMainWindow):
    def __init__(self, user_id, user_repository, panel_view):
        super().__init__()
        self.user_id = user_id
        self.user_repository = user_repository
        self.product_repository = ProductRepository(user_repository.conn)
        self.product_service = ProductService(self.product_repository, self.user_repository)
        self.panel_view = panel_view
        self.setWindowTitle("Product List")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Add header widget separately
        self.header_widget = QWidget()
        self.layout.addWidget(self.header_widget)

        self.product_list = QListWidget()
        self.product_list.setSelectionMode(QListWidget.SingleSelection)
        self.product_list.itemClicked.connect(self.on_product_selected)
        self.product_list.setFont(QFont("Courier New", 10))
        self.product_list.setStyleSheet("""
            QListWidget {
                background-color: #2e2e2e;
                border-radius: 5px;
                padding: 5px;
                color: white;
            }
            QListWidget::item {
                border-bottom: 1px solid #555555;
                padding: 8px;
                background-color: #3a3a3a;
                margin: 2px;
                border-radius: 3px;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #4a90e2;
                border: 1px solid #a0a0a0;
                color: white;
            }
        """)
        self.product_list.setMinimumWidth(500)
        self.layout.addWidget(self.product_list)

        # Form layout for product details
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

        # Load header and products
        self.add_list_header()
        self.load_products()

    def add_list_header(self):
        header_layout = QHBoxLayout(self.header_widget)

        labels = ["Product Name", "Company Name", "Price", "Quantity"]
        widths = [150, 150, 100, 80]

        for label, width in zip(labels, widths):
            lbl = QLabel(label)
            lbl.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    font-size: 12px;
                    color: white;
                }
            """)
            lbl.setMinimumWidth(width)
            header_layout.addWidget(lbl)

        self.header_widget.setStyleSheet("""
            background-color: #4a4a4a;
            border-radius: 3px;
            padding: 5px;
        """)

    def load_products(self, item=None):
        self.product_list.clear()

        products = self.product_service.get_user_products(self.user_id)
        for product in products:
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(5, 5, 5, 5)

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
                        color: white;
                    }
                """)
                lbl.setMinimumWidth(width)
                item_layout.addWidget(lbl)

            list_item = QListWidgetItem()
            list_item.setSizeHint(QSize(0, 40))
            list_item.setData(Qt.UserRole, product.product_id)
            self.product_list.addItem(list_item)
            self.product_list.setItemWidget(list_item, item_widget)

    # Other methods remain the same...
    def load_products(self, item=None):
        self.product_list.clear()
        self.add_list_header()

        products = self.product_service.get_user_products(self.user_id)
        for product in products:
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(5, 5, 5, 5)

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
                        color: white;  /* White text for items */
                    }
                """)
                lbl.setMinimumWidth(width)
                item_layout.addWidget(lbl)

            list_item = QListWidgetItem()
            list_item.setSizeHint(QSize(0, 40))
            list_item.setData(Qt.UserRole, product.product_id)  # Store product ID
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

        try:
            self.product_service.add_product(category, name, company_name, price, quantity, exp_date, self.user_id)
            self.load_products()
            self.clear_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def edit_product(self):
        selected_item = self.product_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "Select a product to edit")
            return
        product_id = selected_item.data(Qt.UserRole)
        if not product_id:
            QMessageBox.warning(self, "Error", "Invalid product selected")
            return

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

        try:
            self.product_service.update_product(product_id, category, name, company_name, price, quantity, exp_date)
            self.load_products()
            self.clear_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def delete_product(self):
        selected_item = self.product_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "Select a product to delete")
            return
        product_id = selected_item.data(Qt.UserRole)
        if not product_id:
            QMessageBox.warning(self, "Error", "Invalid product selected")
            return

        try:
            self.product_service.delete_product(product_id)
            self.load_products()
            self.clear_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

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

    def on_product_selected(self, item: QListWidgetItem):
        """When the user clicks a row, load its values into the form."""
        product_id = item.data(Qt.UserRole)
        prod = self.product_repository.get_product_by_id(product_id)
        if not prod:
            return

        # Populate category dropdown
        idx = self.category_input.findText(prod.category)
        self.category_input.setCurrentIndex(idx if idx >= 0 else 0)

        # Populate text fields
        self.name_input.setText(prod.name)
        self.company_name_input.setText(prod.company_name)
        self.price_input.setText(str(prod.price))
        self.quantity_input.setValue(prod.quantity)

        # Populate expiration date
        date = QDate.fromString(prod.exp_date, "yyyy-MM-dd")
        self.exp_date_input.setDate(date if date.isValid() else QDate.currentDate())
