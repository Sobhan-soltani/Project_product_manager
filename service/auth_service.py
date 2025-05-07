from model.user import User
import sqlite3

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def signup(self, name, family, birthdate, national_code, phone_number, username, password):
        try:
            if self.user_repository.get_user_by_username(username):
                raise ValueError("Username already exists")
            user = User(None, name, family, birthdate, national_code, phone_number, username, password)
            user_id = self.user_repository.save_user(user)
            return user_id
        except sqlite3.OperationalError as e:
            raise RuntimeError(f"Database error during signup: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during signup: {e}")

    def login(self, username, password):
        try:
            user = self.user_repository.get_user_by_username(username)
            if user and user.password == password:
                return user
            return None
        except sqlite3.OperationalError as e:
            raise RuntimeError(f"Database error during login: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during login: {e}")