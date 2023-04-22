from flask_restx import fields, Resource

from extensions import db
from extensions.flask_restx_extension import userNS
from models import User


card_model = userNS.model('Card', {
    'id': fields.Integer(readonly=True),
    'cardNumber': fields.String,
    'user_id': fields.Integer,
})

user_model = userNS.model('User', {
    'id': fields.Integer(readonly=True),
    'password': fields.String,
    'email': fields.String,
    'role': fields.String,
    'cards': fields.Nested(card_model)
})


class UserResourceList(Resource):
    @userNS.marshal_list_with(user_model)
    def get(self):
        user = User.query.all()
        return user

    @userNS.expect(user_model)
    def post(self):
        user = User(**userNS.payload)
        db.session.add(user)
        db.session.commit()
        return {'result': 'success'}


class UserResource(Resource):
    @userNS.marshal_with(user_model)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            userNS.abort(404, 'User not found')
        return user

    @userNS.expect(user_model)
    def put(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            userNS.abort(404, 'User not found')
        user.password = userNS.payload['password']
        user.email = userNS.payload['email']
        user.role = userNS.payload['role']
        db.session.commit()
        return {'result': 'success'}

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            userNS.abort(404, 'User not found')
        db.session.delete(user)
        db.session.commit()
        return {'result': 'success'}
