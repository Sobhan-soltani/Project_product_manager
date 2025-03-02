# repository/user_repository.py
import sqlite3
import os
from model.user import User

class UserRepository:
    def __init__(self, db_file='repository/users.db'):
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        self.conn = sqlite3.connect(db_file)
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
        self.conn.commit()

    def save_user(self, user):
        try:
            self.cursor.execute('''
                INSERT INTO users (name, family, birthdate, national_code, phone_number, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user.name, user.family, user.birthdate, user.national_code, user.phone_number, user.username, user.password))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")

    def get_user_by_username(self, username):
        self.cursor.execute('''
            SELECT id, name, family, birthdate, national_code, phone_number, username, password
            FROM users WHERE username = ?
        ''', (username,))
        row = self.cursor.fetchone()
        if row:
            return User(*row)
        return None