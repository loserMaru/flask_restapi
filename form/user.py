from flask_restx import fields, Resource

from extensions import db
from extensions.flask_restx_extension import userNS, api
from models import User
from schemas import UserSchema
from marshmallow.exceptions import ValidationError

user_schema = UserSchema()

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
        user = User(password=api.payload.get('password'),
                    email=api.payload.get('email'),
                    role=api.payload.get('role'))
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201


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
