from flask_jwt_extended import create_access_token
from flask_restx import Resource
from flask import request

from extensions import userNS
from models import User


@userNS.route('/login', methods=['POST'])
class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401
