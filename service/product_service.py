# service/product_service.py
from model.product import Product

class ProductService:
    def __init__(self, product_repository, user_repository):
        self.product_repository = product_repository
        self.user_repository = user_repository

    def validate_user(self, user_id):
        """Check if the user exists."""
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} does not exist")
        return user

    def add_product(self, category, name, company_name, price, quantity, exp_date, user_id):
        self.validate_user(user_id)
        product = Product(None, category, name, company_name, price, quantity, exp_date, user_id)
        return self.product_repository.add_product(product)

    def update_product(self, product_id, category, name, company_name, price, quantity, exp_date):
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        product.category = category
        product.name = name
        product.company_name = company_name
        product.price = price
        product.quantity = quantity
        product.exp_date = exp_date
        success = self.product_repository.update_product(product)
        if not success:
            raise ValueError(f"Failed to update product with ID {product_id}")
        return product

    def delete_product(self, product_id):
        success = self.product_repository.delete_product(product_id)
        if not success:
            raise ValueError(f"Product with ID {product_id} not found")
        return True

    def get_user_products(self, user_id):
        self.validate_user(user_id)
        return self.product_repository.get_products_by_user(user_id)

    def purchase_product(self, product_id, quantity):
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        if product.quantity < quantity:
            raise ValueError(f"Not enough stock for '{product.name}'. Available: {product.quantity}")
        new_quantity = product.quantity - quantity
        success = self.product_repository.update_quantity(product_id, new_quantity)
        if not success:
            raise ValueError(f"Failed to update quantity for product with ID {product_id}")
        # Reload the product to get the updated quantity
        product = self.product_repository.get_product_by_id(product_id)
        total_cost = product.price * quantity
        return product, total_cost