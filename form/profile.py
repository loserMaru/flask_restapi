import os

from flask import request
from flask_restx import fields, Resource
from imgurpython import ImgurClient

from extensions import api, db, jwt_required_class
from extensions.flask_restx_extension import profileNS
from form.validations import num_is_valid
from models import Profile
from schemas import ProfileSchema

# from werkzeug.datastructures import FileStorage

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


@jwt_required_class
class ProfileResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @profileNS.doc(security='jwt')
    @profileNS.marshal_list_with(profile_model)
    def get(self):
        """Get a list of profiles"""
        profiles = Profile.query.all()
        return profiles, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресурса',
        400: 'Некорректный запрос'
    })
    @profileNS.expect(profile_model)
    @profileNS.doc(security='jwt')
    # @profileNS.expect(upload_parser)
    def post(self):
        """Create new profile"""
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


@jwt_required_class
class ProfileResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресурс не найден'
    })
    @profileNS.doc(security='jwt')
    @profileNS.marshal_with(profile_model)
    def get(self, id):
        """Get profile by ID"""
        profile = Profile.query.filter_by(id=id).first()
        if not profile:
            profileNS.abort(404, 'Профиль не найден')
        return profile, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресурс не найден'
    })
    @profileNS.doc(security='jwt')
    @profileNS.expect(profile_model)
    def put(self, id):
        """Edit profile by ID"""
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
    @profileNS.doc(security='jwt')
    def delete(self, id):
        """Delete profile by ID"""
        profile = Profile.query.filter_by(id=id).first()
        if not profile:
            profileNS.abort(404, 'Профиль не найден')
        db.session.delete(profile)
        db.session.commit()
        return {'msg': 'Профиль удален успешно'}, 200


@profileNS.doc(security='jwt')
class UploadProfilePic(Resource):
    @profileNS.doc(security='jwt')
    @profileNS.expect(profileNS.parser().add_argument('image', location='files', type='file'))
    def put(self, id):
        """Give picture for profile by his ID"""
        profile = Profile.query.filter_by(id=id).first()
        if not profile:
            profileNS.abort(404, 'Профиль не найден')

        client_id = '7ac7ce010e34893'
        client_secret = '9d2d06f3d8801a800ebf8411f69e898eb667d779'

        client = ImgurClient(client_id, client_secret)

        image = request.files.get('image')
        print(image)
        if not image:
            return {'message': 'No image uploaded'}, 400

        # Save the image to a temporary directory
        temp_dir = os.path.join(os.getcwd(), 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        image_path = os.path.join(temp_dir, image.filename)
        image.save(image_path)

        # Upload the image to imgur
        response = client.upload_from_path(image_path)

        # Remove the temporary file
        os.remove(image_path)

        # Update profile picture
        profile.picture = response['link']
        db.session.commit()

        return profile_schema.dump(profile), 201
