import os

from flask import request, jsonify
from werkzeug.utils import secure_filename

from extensions.flask_uploads_extension import allowed_file


def upload_file(app):
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No files were uploaded'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')

    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'

    if success and errors:
        errors['message'] = 'file(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
