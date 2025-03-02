# main.py
import sys
from PySide6.QtWidgets import QApplication
from repository.user_repository import UserRepository
from service.auth_service import AuthService
from view.login_signup_view import LoginSignupView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)
    login_signup_view = LoginSignupView(auth_service, user_repo)
    login_signup_view.show()
    sys.exit(app.exec())