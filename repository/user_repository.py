# repository/user_repository.py
import sqlite3
import os
from model.user import User
from model.order import Order
from model.payment import Payment
from model.order_item import OrderItem
from model.product import Product

class UserRepository:
    def __init__(self, db_file='repository/users.db'):
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                family TEXT,
                birthdate TEXT,
                national_code TEXT,
                phone_number TEXT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                name TEXT,
                company_name TEXT,
                price REAL,
                quantity INTEGER,
                exp_date TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date_time TEXT,
                total_cost REAL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                payment_type TEXT,
                amount REAL,
                date_time TEXT,
                description TEXT,
                status TEXT,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        ''')
        self.conn.commit()

    def save_user(self, user):
        try:
            self.cursor.execute('''
                INSERT INTO users (name, family, birthdate, national_code, phone_number, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user.name, user.family, user.birthdate, user.national_code, user.phone_number, user.username, user.password))
            self.conn.commit()
            user.id = self.cursor.lastrowid
            return user.id
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")

    def get_user_by_username(self, username):
        self.cursor.execute('''
            SELECT id, name, family, birthdate, national_code, phone_number, username, password
            FROM users WHERE username = ?
        ''', (username,))
        row = self.cursor.fetchone()
        if row:
            return User(row['id'], row['name'], row['family'], row['birthdate'], row['national_code'], row['phone_number'], row['username'], row['password'])
        return None

    def get_user_by_id(self, user_id):
        self.cursor.execute('''
            SELECT id, name, family, birthdate, national_code, phone_number, username, password
            FROM users WHERE id = ?
        ''', (user_id,))
        row = self.cursor.fetchone()
        if row:
            return User(row['id'], row['name'], row['family'], row['birthdate'], row['national_code'], row['phone_number'], row['username'], row['password'])
        return None

    def close(self):
        self.conn.close()