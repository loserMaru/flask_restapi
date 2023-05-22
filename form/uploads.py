import os

from flask import request
from flask_restx import Resource
from imgurpython import ImgurClient

client_id = '38987fafe27568b'


class UploadImage(Resource):
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

        return {'link': response['link']}, 201
