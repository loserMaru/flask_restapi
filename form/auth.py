from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask_restx import Resource, fields

from extensions import loginNS
from extensions.flask_restx_extension import authNS
from form.validations import is_valid_email, password_is_valid, verify_password
from models import User
from schemas import UserSchema

login_model = loginNS.model('Login', {
    'email': fields.String(required=True, default='string@gmail.com'),
    'password': fields.String(required=True)
})

JWT_SECRET_KEY = 'super-secret-key'
user_schema = UserSchema()


class AuthResource(Resource):
    @authNS.expect(login_model)
    def post(self):
        """Login and get access and refresh tokens"""
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not is_valid_email(email):
            authNS.abort(400, 'Некорректный email')
        if not password_is_valid(password):
            authNS.abort(400, 'Некорректный пароль')

        user = User.query.filter_by(email=email).first()
        if not user:
            authNS.abort(401, 'Неправильный email или пароль')

        if not verify_password(password, user.password):
            authNS.abort(401, 'Неправильный email или пароль')

        # Generate JWT token
        access_token = create_access_token(identity=user.to_dict())
        refresh_token = create_refresh_token(identity=user.to_dict())

        return {'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()}, 200


class TokenRefresh(Resource):
    @authNS.doc(security='jwt')
    @jwt_required(refresh=True)
    def post(self):
        """Refresh access tokens"""
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 200
