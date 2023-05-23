import re

from flask_bcrypt import generate_password_hash, check_password_hash


def num_is_valid(number):
    """Проверка номера телефона на соответствие российскому формату"""
    regex = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    return bool(re.match(regex, number))


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def password_is_valid(password):
    if not password:
        return False
    return len(password) >= 8


def hash_password(password):
    return generate_password_hash(password)


def verify_password(password, hash):
    return check_password_hash(hash, password)
