from model.user import User

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def signup(self, name, family, birthdate, national_code, phone_number, username, password):
        if self.user_repository.get_user_by_username(username):
            raise ValueError("Username already exists")
        user = User(None, name, family, birthdate, national_code, phone_number, username, password)
        self.user_repository.save_user(user)

    def login(self, username, password):
        user = self.user_repository.get_user_by_username(username)
        if user and user.password == password:
            return user
        return None