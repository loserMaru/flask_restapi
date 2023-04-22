from flask_restx import fields, Resource

from extensions import api, db
from extensions.flask_restx_extension import profileNS
from models.models import Profile


profile_model = profileNS.model('Profile', {
    'id': fields.Integer(readonly=True),
    'nickname': fields.String(required=True),
    'picture': fields.String(),
    'phone': fields.String(required=True),
    'user_id': fields.Integer(required=True),
})


class ProfileResourceList(Resource):
    @profileNS.marshal_list_with(profile_model)
    def get(self):
        profiles = Profile.query.all()
        return profiles

    @profileNS.expect(profile_model)
    def post(self):
        profile = Profile(**profileNS.payload)
        db.session.add(profile)
        db.session.commit()
        return {'result': 'success'}


class ProfileResource(Resource):
    @profileNS.marshal_with(profile_model)
    def get(self, profile_id):
        profile = Profile.query.filter_by(id=profile_id).first()
        if not profile:
            profileNS.abort(404, 'Profile not found')
        return profile

    @profileNS.expect(profile_model)
    def put(self, profile_id):
        profile = Profile.query.filter_by(id=profile_id).first()
        if not profile:
            profileNS.abort(404, 'Profile not found')
        for key, value in profileNS.payload.items():
            setattr(profile, key, value)
        db.session.commit()
        return {'result': 'success'}

    def delete(self, profile_id):
        profile = Profile.query.filter_by(id=profile_id).first()
        if not profile:
            profileNS.abort(404, 'Profile not found')
        db.session.delete(profile)
        db.session.commit()
        return {'result': 'success'}
