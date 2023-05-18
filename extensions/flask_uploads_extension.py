import os

ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])
UPLOAD_FOLDER = 'static/upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
