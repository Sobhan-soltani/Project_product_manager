# main.py
import sys
from PySide6.QtWidgets import QApplication
from repository.user_repository import UserRepository
from repository.product_repository import ProductRepository
from repository.order_repository import OrderRepository
from service.auth_service import AuthService
from service.product_service import ProductService
from service.order_service import OrderService
from view.login_signup_view import LoginSignupView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Initialize repositories
    user_repo = UserRepository()
    product_repo = ProductRepository(user_repo.conn)
    order_repo = OrderRepository(user_repo.conn)

    # Initialize services
    auth_service = AuthService(user_repo)
    product_service = ProductService(product_repo, user_repo)
    order_service = OrderService(order_repo, product_service)

    # Launch the login/signup view
    login_signup_view = LoginSignupView(auth_service, user_repo, product_service, order_service)
    login_signup_view.show()

    sys.exit(app.exec())