import os

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource
from imgurpython import ImgurClient

from extensions import uploadNS, db, jwt_required_class
from models import User, Profile


@jwt_required_class
class UploadImage(Resource):
    @uploadNS.expect(uploadNS.parser().add_argument('image', location='files', type='file'))
    @uploadNS.doc(security='jwt')
    def post(self):
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

        # Update the user's profile picture with the link
        user_id = get_jwt_identity().get('id')
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'Пользователь не найден'}, 404

        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            profile = Profile(user_id=user_id)

        profile.picture = response['link']
        db.session.add(profile)
        db.session.commit()

        return {'link': response['link']}, 201
