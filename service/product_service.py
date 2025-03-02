# service/product_service.py
from model.product import Product

class ProductService:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def add_product(self, category, name, company_name, price, quantity, exp_date, user_id):
        product = Product(None, category, name, company_name, price, quantity, exp_date, user_id)
        return self.product_repository.add_product(product)

    def update_product(self, product_id, category, name, company_name, price, quantity, exp_date):
        product = Product(product_id, category, name, company_name, price, quantity, exp_date, None)
        self.product_repository.update_product(product)

    def delete_product(self, product_id):
        self.product_repository.delete_product(product_id)

    def get_user_products(self, user_id):
        return self.product_repository.get_products_by_user(user_id)