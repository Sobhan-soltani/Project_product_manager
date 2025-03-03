# model/product.py
class Product:
    def __init__(self, id, category, name, company_name, price,  exp_date):
        self.id = id
        self.category = category
        self.name = name
        self.company_name = company_name
        self.price = price
        self.exp_date = exp_date

    def __repr__(self):
        return f"{self.__dict__}"