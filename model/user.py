class User:
    def __init__(self, id, name, family, birthdate, national_code, phone_number, username, password):
        self.id = id
        self.name = name
        self.family = family
        self.birthdate = birthdate
        self.national_code = national_code
        self.phone_number = phone_number
        self.username = username
        self.password = password

    def __repr__(self):
        return f"{self.__dict__}"