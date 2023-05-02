import sqlalchemy
from flask_bcrypt import Bcrypt
from flask_restx import fields, Resource

from extensions import db
from extensions.flask_restx_extension import userNS, api
from form.validations import is_valid_email
from models import User
from schemas import UserSchema

user_schema = UserSchema()
bcrypt = Bcrypt()

user_model = userNS.model('User', {
    'id': fields.Integer(readonly=True),
    'email': fields.String(default='string@gmail.com'),
    'password': fields.String,
    'confirm_password': fields.String,
    'role': fields.String(default='user'),
})


class UserResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @userNS.marshal_list_with(user_model, skip_none=True)
    def get(self):
        users = User.query.all()
        return users, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресурса',
        400: 'Некорректный запрос'
    })
    @userNS.expect(user_model)
    @userNS.marshal_with(user_model, code=201, skip_none=True)
    def post(self):
        email = api.payload.get('email')
        if not is_valid_email(email):
            userNS.abort(400, 'Некорректный email')
        password = api.payload.get('password')
        confirm_password = api.payload.get('confirm_password')
        if confirm_password != password or not confirm_password:
            userNS.abort(400, 'Пароли не совпадают')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(password=hashed_password,
                    email=email,
                    role=api.payload.get('role'))
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        del user_model['confirm_password']
        return user_schema.dump(user), 201


class UserResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресурс не найден'
    })
    @userNS.marshal_with(user_model, skip_none=True)
    def get(self, id):
        user = User.query.get(id)
        if not user:
            api.abort(404, 'User not found')
        return user, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресурс не найден'
    })
    @userNS.expect(user_model, skip_none=True)
    def put(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            api.abort(404, 'User not found')
        user.password = userNS.payload['password']
        user.password = bcrypt.generate_password_hash(user.password).decode('utf-8')
        user.email = userNS.payload['email']
        user.role = userNS.payload['role']
        db.session.commit()
        return user_schema.dump(user), 200

    @api.doc(responses={
        200: 'Успешный DELETE-запрос, ресурс удален',
        401: 'Неавторизованный доступ',
        404: 'Ресурс не найден'
    })
    def delete(self, id):
        user = User.query.get(id)
        if not user:
            api.abort(404, message='Пользователь с id {} не найден'.format(id))
        try:
            db.session.delete(user)
            db.session.commit()
            return {'msg': 'Пользователь удален'}, 200
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return {'msg': 'Ошибка. У пользователя есть внешние ключи'}, 200
