# repository/product_repository.py
from model.product import Product

class ProductRepository:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def add_product(self, product):
        self.cursor.execute('''
            INSERT INTO products (category, name, company_name, price, quantity, exp_date, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (product.category, product.name, product.company_name, product.price, product.quantity, product.exp_date, product.user_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_product(self, product):
        self.cursor.execute('''
            UPDATE products SET category = ?, name = ?, company_name = ?, price = ?, quantity = ?, exp_date = ?
            WHERE id = ?
        ''', (product.category, product.name, product.company_name, product.price, product.quantity, product.exp_date, product.id))
        self.conn.commit()

    def delete_product(self, product_id):
        self.cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        self.conn.commit()

    def get_products_by_user(self, user_id):
        self.cursor.execute('''
            SELECT id, category, name, company_name, price, quantity, exp_date, user_id
            FROM products WHERE user_id = ?
        ''', (user_id,))
        rows = self.cursor.fetchall()
        return [Product(*row) for row in rows]