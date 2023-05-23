from flask import request
from flask_restx import fields, Resource, reqparse, inputs
# from werkzeug.datastructures import FileStorage

from extensions import api, db
from extensions.flask_restx_extension import profileNS
from form.validations import num_is_valid
from models import Profile
from schemas import ProfileSchema

profile_model = profileNS.model('Profile', {
    'id': fields.Integer(readonly=True),
    'nickname': fields.String(required=True),
    'picture': fields.String(),
    'phone': fields.String(required=True),
    'user_id': fields.Integer(required=True),
})

profile_schema = ProfileSchema()

# upload_parser = reqparse.RequestParser()
# upload_parser.add_argument('image', type=FileStorage, location='files', required=True, help='Image file (required)')
# upload_parser.add_argument('nickname', type=str, required=True, help='Nickname (required)')
# upload_parser.add_argument('phone', type=str, required=True, help='Phone number (required)')
# upload_parser.add_argument('user_id', type=int, required=True, help='User ID (required)')


class ProfileResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @profileNS.marshal_list_with(profile_model)
    def get(self):
        profiles = Profile.query.all()
        return profiles, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресурса',
        400: 'Некорректный запрос'
    })
    @profileNS.expect(profile_model)
    # @profileNS.expect(upload_parser)
    def post(self):
        data = request.json
        # image = request.files.get('picture')
        phone = profileNS.payload.get('phone')
        if not num_is_valid(phone):
            profileNS.abort(400, 'Неправильный номер телефона')
        profile = Profile(
            nickname=data['nickname'],
            picture=data['picture'],
            phone=data['phone'],
            user_id=data['user_id']
        )
        db.session.add(profile)
        db.session.commit()
        return profile_schema.dump(profile), 201


class ProfileResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресурс не найден'
    })
    @profileNS.marshal_with(profile_model)
    def get(self, id):
        profile = Profile.query.filter_by(id=id).first()
        if not profile:
            profileNS.abort(404, 'Профиль не найден')
        return profile, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресурс не найден'
    })
    @profileNS.expect(profile_model)
    def put(self, id):
        profile = Profile.query.filter_by(id=id).first()
        if not profile:
            profileNS.abort(404, 'Профиль не найден')
        phone = profileNS.payload.get('phone')
        if not num_is_valid(phone):
            profileNS.abort(404, 'Неправильный номер телефона')
        for key, value in profileNS.payload.items():
            setattr(profile, key, value)
        db.session.commit()
        return profile.to_dict(), 200

    @api.doc(responses={
        200: 'Успешный DELETE-запрос, ресурс удален',
        404: 'Ресурс не найден'
    })
    def delete(self, id):
        profile = Profile.query.filter_by(id=id).first()
        if not profile:
            profileNS.abort(404, 'Профиль не найден')
        db.session.delete(profile)
        db.session.commit()
        return {'msg': 'Профиль удален успешно'}, 200
