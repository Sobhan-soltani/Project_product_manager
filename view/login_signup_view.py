# view/login_signup_view.py
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QTabWidget, QLineEdit, QPushButton, QMessageBox, QDateEdit)
from validation.validator import is_valid_username  #is_valid_password
from view.panel_view import PanelView

class LoginSignupView(QMainWindow):
    def __init__(self, auth_service, user_repository):
        super().__init__()
        self.auth_service = auth_service
        self.user_repository = user_repository
        self.setWindowTitle("Login / Signup")
        self.setGeometry(100, 100, 400, 400)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.login_tab = QWidget()
        self.signup_tab = QWidget()
        self.tab_widget.addTab(self.login_tab, "Login")
        self.tab_widget.addTab(self.signup_tab, "Signup")

        self.setup_login_tab()
        self.setup_signup_tab()

    def setup_login_tab(self):
        layout = QVBoxLayout()
        self.login_username_input = QLineEdit()
        self.login_username_input.setPlaceholderText("Username")
        layout.addWidget(self.login_username_input)

        self.login_password_input = QLineEdit()
        self.login_password_input.setPlaceholderText("Password")
        self.login_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.login_password_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)

        back_button = QPushButton("Exit")
        back_button.clicked.connect(self.close)  # Closes the app
        layout.addWidget(back_button)

        self.login_tab.setLayout(layout)

    def setup_signup_tab(self):
        layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        layout.addWidget(self.name_input)

        self.family_input = QLineEdit()
        self.family_input.setPlaceholderText("Family")
        layout.addWidget(self.family_input)

        self.birthdate_input = QDateEdit()
        self.birthdate_input.setCalendarPopup(True)
        layout.addWidget(self.birthdate_input)

        self.national_code_input = QLineEdit()
        self.national_code_input.setPlaceholderText("National Code")
        layout.addWidget(self.national_code_input)

        self.phone_number_input = QLineEdit()
        self.phone_number_input.setPlaceholderText("Phone Number")
        layout.addWidget(self.phone_number_input)

        self.signup_username_input = QLineEdit()
        self.signup_username_input.setPlaceholderText("Username")
        layout.addWidget(self.signup_username_input)

        self.signup_password_input = QLineEdit()
        self.signup_password_input.setPlaceholderText("Password")
        self.signup_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.signup_password_input)

        signup_button = QPushButton("Signup")
        signup_button.clicked.connect(self.handle_signup)
        layout.addWidget(signup_button)

        back_button = QPushButton("Exit")
        back_button.clicked.connect(self.close)  # Closes the app
        layout.addWidget(back_button)

        self.signup_tab.setLayout(layout)

    def handle_login(self):
        username = self.login_username_input.text()
        password = self.login_password_input.text()
        user = self.auth_service.login(username, password)
        if user:
            self.open_panel(user.id)
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def handle_signup(self):
        name = self.name_input.text()
        family = self.family_input.text()
        birthdate = self.birthdate_input.date().toString("yyyy-MM-dd")
        national_code = self.national_code_input.text()
        phone_number = self.phone_number_input.text()
        username = self.signup_username_input.text()
        password = self.signup_password_input.text()

        if not all([name, family, national_code, phone_number, username, password]):
            QMessageBox.warning(self, "Error", "All fields are required")
            return

        if not is_valid_username(username):
            QMessageBox.warning(self, "Error", "Username must be 3-20 alphanumeric characters")
            return

        # if not is_valid_password(password):
        #     QMessageBox.warning(self, "Error", "Password must be 8+ characters with upper, lower, and digits")
        #     return

        try:
            self.auth_service.signup(name, family, birthdate, national_code, phone_number, username, password)
            QMessageBox.information(self, "Success", "Signup successful. Please log in.")
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def open_panel(self, user_id):
        self.panel_view = PanelView(user_id, self.user_repository, self)
        self.panel_view.show()
        self.hide()