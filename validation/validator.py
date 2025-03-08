import re

def is_valid_username(username):
    return re.match(r'^[a-zA-Z0-9]{3,20}$', username) is not None
#
# def is_valid_password(password):
#     return (len(password) >= 8 and
#             any(c.isupper() for c in password) and
#             any(c.islower() for c in password) and
#             any(c.isdigit() for c in password))