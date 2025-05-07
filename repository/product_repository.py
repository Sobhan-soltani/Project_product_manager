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
        product.product_id = self.cursor.lastrowid
        return product.product_id

    def update_product(self, product):
        self.cursor.execute('''
            UPDATE products SET category = ?, name = ?, company_name = ?, price = ?, quantity = ?, exp_date = ?, user_id = ?
            WHERE id = ?
        ''', (product.category, product.name, product.company_name, product.price, product.quantity, product.exp_date, product.user_id, product.product_id))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def update_quantity(self, product_id, quantity):
        self.cursor.execute('''
            UPDATE products SET quantity = ?
            WHERE id = ?
        ''', (quantity, product_id))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_product(self, product_id):
        self.cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_products_by_user(self, user_id):
        self.cursor.execute('''
            SELECT id, category, name, company_name, price, quantity, exp_date, user_id
            FROM products WHERE user_id = ?
        ''', (user_id,))
        rows = self.cursor.fetchall()
        return [Product(row['id'], row['category'], row['name'], row['company_name'], row['price'], row['quantity'], row['exp_date'], row['user_id']) for row in rows]

    def get_product_by_id(self, product_id):
        self.cursor.execute('''
            SELECT id, category, name, company_name, price, quantity, exp_date, user_id
            FROM products WHERE id = ?
        ''', (product_id,))
        row = self.cursor.fetchone()
        if row:
            return Product(row['id'], row['category'], row['name'], row['company_name'], row['price'], row['quantity'], row['exp_date'], row['user_id'])
        return None