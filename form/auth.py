from flask_bcrypt import check_password_hash
from functools import wraps

from flask import request, jsonify

from models import User


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not authenticate(auth.username, auth.password):
            return jsonify({'message': 'Unauthorized access'}), 401
        return f(*args, **kwargs)

    return decorated_function
