from flask import request
from flask_restx import Resource

from form.imgbb_upload import upload_image_to_imgur

client_id = '38987fafe27568b'


class UploadImage(Resource):
    def post(self):
        image = request.files['image']
        image.save('temp_image.jpg')  # Сохраняем загруженное изображение временно на сервере
        image_url = upload_image_to_imgur('temp_image.jpg', client_id)
        # Удаление временного изображения, если требуется
        # os.remove('temp_image.jpg')

        if image_url:
            return {'image_url': image_url}
        else:
            return {'message': 'Image upload failed'}, 500
