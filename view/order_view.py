# view/order_view.py

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QLabel,
    QSpinBox, QPushButton, QMessageBox,
    QWidget
)
from PySide6.QtGui import QPixmap  # برای نمایش تصویر


class OrderView(QDialog):
    def __init__(self, user, order_service, product_service, panel_view):
        super().__init__()
        self.user = user
        self.order_service = order_service
        self.product_service = product_service
        self.panel_view = panel_view

        self.setWindowTitle("Order View")
        self.setGeometry(100, 100, 800, 600)

        if not self.user:
            QMessageBox.critical(self, "Error", "Not logged in – please login again.")
            self.close()
            return

        # ─── Main Layout ───────────────────────────────
        outer = QHBoxLayout(self)

        # ─── Left Column ───────────────────────────────
        left_col = QVBoxLayout()

        # Title
        lbl_title = QLabel("Available Products:")
        left_col.addWidget(lbl_title)

        # Header (outside the list)
        hdr = QWidget()
        hdr.setStyleSheet("""
            background-color: #4a4a4a;
            border-radius: 3px;
            padding: 5px;
        """)
        hdr_lay = QHBoxLayout(hdr)
        hdr_lay.setContentsMargins(5,5,5,5)
        for text, w in [("Name", 100), ("Company", 100), ("Price", 80), ("Stock", 80)]:
            l = QLabel(text)
            l.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    font-size: 12px;
                    color: white;
                }
            """)
            l.setMinimumWidth(w)
            hdr_lay.addWidget(l)
        left_col.addWidget(hdr)

        # The product list itself
        self.product_list = QListWidget()
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
        self.product_list.setMinimumWidth(400)
        self.product_list.itemClicked.connect(self.select_product)
        left_col.addWidget(self.product_list)

        # Empty label for when no products are available
        self.empty_label = QLabel("No products available.")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                padding: 20px;
            }
        """)
        self.empty_label.hide()
        left_col.addWidget(self.empty_label)

        outer.addLayout(left_col)

        # ─── Right Column ──────────────────────────────
        right_col = QVBoxLayout()

        # Image Label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #3a3a3a;
                border-radius: 5px;
                padding: 20px;
                font-size: 24px;
                color: white;
            }
        """)
        self.image_label.setText("Image")
        right_col.addWidget(self.image_label)

        # Past orders
        self.order_list = QListWidget()
        self.order_list.setStyleSheet("""
            QListWidget {
                background-color: #2e2e2e;
                border-radius: 5px;
                padding: 5px;
                color: white;
            }
            QListWidget::item {
                padding: 8px;
                color: white;
            }
        """)
        self.order_list.setMinimumHeight(300)
        self.order_list.setMinimumWidth(350)
        right_col.addWidget(self.order_list)

        # Form for new order
        form = QVBoxLayout()
        self.sel_lbl    = QLabel("Selected Product: None")
        self.price_lbl  = QLabel("Price: N/A")
        self.stock_lbl  = QLabel("Stock: N/A")  # New field for stock
        form.addWidget(self.sel_lbl)
        form.addWidget(self.price_lbl)
        form.addWidget(self.stock_lbl)

        ql = QHBoxLayout()
        ql.addWidget(QLabel("Quantity:"))
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, 10000)
        ql.addWidget(self.qty_spin)
        form.addLayout(ql)

        # Order details after save
        self.id_lbl    = QLabel("Order ID: N/A")
        self.date_lbl  = QLabel("Date: N/A")
        self.total_lbl = QLabel("Total Price: N/A")
        for w in (self.id_lbl, self.date_lbl, self.total_lbl):
            form.addWidget(w)

        right_col.addLayout(form)

        # Buttons
        btns = QHBoxLayout()
        self.save_btn   = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.back_btn   = QPushButton("Back")
        self.save_btn.clicked.connect(self.save_order)
        self.cancel_btn.clicked.connect(self.cancel)
        self.back_btn.clicked.connect(self.go_back)
        for b in (self.save_btn, self.cancel_btn, self.back_btn):
            btns.addWidget(b)
        right_col.addLayout(btns)

        outer.addLayout(right_col)

        # State
        self.selected_product = None

        # Load data
        self.load_products()
        self.load_orders()

    def load_products(self):
        """Just repopulate the list—header lives above."""
        self.product_list.clear()
        products = self.product_service.get_user_products(self.user.id)



        self.empty_label.hide()
        self.product_list.show()

        for p in products:
            row = QWidget()
            lay = QHBoxLayout(row)
            lay.setContentsMargins(5,5,5,5)
            for text, w in [
                (p.name, 100),
                (p.company_name, 100),
                (f"${p.price:.2f}", 80),
                (str(p.quantity), 80)
            ]:
                lbl = QLabel(text)
                lbl.setStyleSheet("""
                    QLabel { font-size: 12px; color: white; }
                """)
                lbl.setMinimumWidth(w)
                lay.addWidget(lbl)

            item = QListWidgetItem()
            item.setSizeHint(row.sizeHint())
            item.setData(Qt.UserRole, p)
            self.product_list.addItem(item)
            self.product_list.setItemWidget(item, row)

    def select_product(self, item):
        p = item.data(Qt.UserRole)
        self.selected_product = p

        # Hide product list and show image + info
        self.product_list.hide()
        self.empty_label.hide()

        self.sel_lbl.setText(f"Selected Product: {p.name}")
        self.price_lbl.setText(f"Price: ${p.price:.2f}")
        self.stock_lbl.setText(f"Stock: {p.quantity}")

        # Show image if available
        if hasattr(p, 'image_path') and p.image_path:
            pixmap = QPixmap(p.image_path).scaled(200, 200, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("Image")

    def load_orders(self):
        self.order_list.clear()
        for o in self.order_service.get_user_orders(self.user.id):
            for oi in o.order_item_list:
                txt = (f"Order #{o.id}  {o.date_time}  "
                       f"{oi.product.name} x{oi.quantity} → "
                       f"${oi.price * oi.quantity:.2f}")
                self.order_list.addItem(txt)

    def save_order(self):
        if not self.selected_product:
            return QMessageBox.warning(self, "Error", "Please select a product.")
        try:
            order, total = self.order_service.create_order(
                self.user, self.selected_product.product_id, self.qty_spin.value()
            )
            self.id_lbl.setText(f"Order ID: {order.id}")
            self.date_lbl.setText(f"Date: {order.date_time}")
            self.total_lbl.setText(f"Total Price: ${total:.2f}")
            QTimer.singleShot(100, lambda: (self.load_orders(), self.load_products()))
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def cancel(self):
        # Clear selection and show product list again
        self.selected_product = None
        self.sel_lbl.setText("Selected Product: None")
        self.price_lbl.setText("Price: N/A")
        self.stock_lbl.setText("Stock: N/A")
        self.qty_spin.setValue(1)
        self.id_lbl.setText("Order ID: N/A")
        self.date_lbl.setText("Date: N/A")
        self.total_lbl.setText("Total Price: N/A")
        self.image_label.setText("Image")
        self.product_list.show()

    def go_back(self):
        self.panel_view.show()
        self.close()