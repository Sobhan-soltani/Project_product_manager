# view/login_signup_view.py
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QPushButton, QMessageBox, QLabel)
from view.panel_view import PanelView

class LoginSignupView(QMainWindow):
    def __init__(self, auth_service, user_repository, product_service, order_service):
        super().__init__()
        self.auth_service = auth_service
        self.user_repository = user_repository
        self.product_service = product_service
        self.order_service = order_service
        self.setWindowTitle("Login / Signup")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.button_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.button_layout.addWidget(self.login_button)

        self.signup_button = QPushButton("Signup")
        self.signup_button.clicked.connect(self.signup)
        self.button_layout.addWidget(self.signup_button)

        self.layout.addLayout(self.button_layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            user = self.auth_service.login(username, password)
            self.panel_view = PanelView(user, self.user_repository, self.product_service, self.order_service)
            self.panel_view.show()
            self.close()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def signup(self):
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            user = self.auth_service.signup(username, password)
            QMessageBox.information(self, "Success", "User created successfully. Please login.")
            self.username_input.clear()
            self.password_input.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))