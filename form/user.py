from flask_bcrypt import Bcrypt
from flask_restx import fields, Resource
from flask import request

from extensions import db
from extensions.flask_restx_extension import userNS, api
from models import User
from schemas import UserSchema

user_schema = UserSchema()
bcrypt = Bcrypt()

card_model = userNS.model('Card', {
    'id': fields.Integer(readonly=True),
    'cardNumber': fields.String,
    'user_id': fields.Integer,
})

user_model = userNS.model('User', {
    'id': fields.Integer(readonly=True),
    'password': fields.String,
    'email': fields.String,
    'role': fields.String(default='user'),
    'cards': fields.Nested(card_model)
})


class UserResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @userNS.marshal_list_with(user_model)
    def get(self):
        users = User.query.all()
        return users, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресурса',
        400: 'Некорректный запрос'
    })
    @userNS.expect(user_model)
    @userNS.marshal_with(user_model, code=201)
    def post(self):
        password = api.payload.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(password=hashed_password,
                    email=api.payload.get('email'),
                    role=api.payload.get('role'),
                    cards=[])
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201


class UserResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресурс не найден'
    })
    @userNS.marshal_with(user_model)
    def get(self, id):
        user = User.query.get(id)
        if not user:
            api.abort(404, 'User not found')
        return user, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресурс не найден'
    })
    @userNS.expect(user_model)
    def put(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            api.abort(404, 'User not found')
        user.password = userNS.payload['password']
        user.email = userNS.payload['email']
        user.role = userNS.payload['role']
        db.session.commit()
        return user_schema.dump(user), 200

    @api.doc(responses={
        204: 'Успешный DELETE-запрос, ресурс удален',
        404: 'Ресурс не найден'
    })
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            api.abort(404, message='Пользователь с id {} не найден'.format(id))
        db.session.delete(user)
        db.session.commit()
        return {'result': 'success'}, 204
