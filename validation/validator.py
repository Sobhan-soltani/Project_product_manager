# validation/validator.py
import re

def is_valid_username(username):
    return bool(re.match(r'^[a-zA-Z0-9]{3,20}$', username))

def is_valid_password(password):
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$', password))

def is_valid_national_code(national_code):
    return bool(re.match(r'^\d{10}$', national_code))

def is_valid_phone_number(phone_number):
    return bool(re.match(r'^\d{10,15}$', phone_number))