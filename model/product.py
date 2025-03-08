# model/product.py
# model/product.py
class Product:
    def __init__(self, product_id, category, name, company_name, price, quantity, exp_date, user_id):
        self.product_id = product_id
        self.category = category
        self.name = name
        self.company_name = company_name
        self.price = price
        self.quantity = quantity
        self.exp_date = exp_date
        self.user_id = user_id

    def __repr__(self):
        return f"{self.__dict__}"