from flask import request, jsonify

from flask_restx import fields, Resource

from extensions import api, db
from extensions.flask_restx_extension import profileNS
from models import Profile
from schemas import profile_schema

profile_model = profileNS.model('Profile', {
    'id': fields.Integer(readonly=True),
    'nickname': fields.String(required=True),
    'picture': fields.String(),
    'phone': fields.String(required=True),
    'user_id': fields.Integer(required=True),
})


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
    def post(self):
        data = request.json
        errors = profile_schema.validate(data)
        if errors:
            return jsonify(errors), 400
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
            profileNS.abort(404, 'Profile not found')
        return profile, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресурс не найден'
    })
    @profileNS.expect(profile_model)
    def put(self, id):
        profile = Profile.query.filter_by(id=id).first()
        if not profile:
            profileNS.abort(404, 'Profile not found')
        for key, value in profileNS.payload.items():
            setattr(profile, key, value)
        db.session.commit()
        return profile.to_dict(), 200

    @api.doc(responses={
        204: 'Успешный DELETE-запрос, ресурс удален',
        404: 'Ресурс не найден'
    })
    def delete(self, id):
        profile = Profile.query.filter_by(id=id).first()
        if not profile:
            profileNS.abort(404, 'Profile not found')
        db.session.delete(profile)
        db.session.commit()
        return {'result': 'success'}, 204
