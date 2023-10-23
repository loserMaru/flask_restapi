import os

import sqlalchemy

from extensions.flask_restx_extension import categoryNS
from models import Category
from flask import request
from flask_restx import fields, Resource
from imgurpython import ImgurClient

from extensions import api, db, jwt_required_class
from schemas import CategorySchema

category_schema = CategorySchema()

category_model = categoryNS.model('Category', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'picture': fields.String(),
})


@jwt_required_class
class CategoryResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @api.marshal_list_with(category_model)
    @categoryNS.doc(security='jwt')
    def get(self):
        """Get a list of categories"""
        categories = Category.query.all()
        return categories, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание новой категории',
        400: 'Некорректный запрос'
    })
    @api.expect(category_model)
    @categoryNS.doc(security='jwt')
    @api.marshal_with(category_model, code=201)
    def post(self):
        """Create new category"""
        category = Category(**api.payload)
        db.session.add(category)
        db.session.commit()
        return category.to_dict(), 201


@jwt_required_class
class CategoryResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Категория не найдена'
    })
    @api.marshal_with(category_model)
    @categoryNS.doc(security='jwt')
    def get(self, id):
        """Get category by ID"""
        category = Category.query.get(id)
        if not category:
            api.abort(404, 'Category not found')
        return category, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Категория не найдена'
    })
    @categoryNS.doc(security='jwt')
    @api.expect(category_model)
    def put(self, id):
        """Edit category by ID"""
        category = Category.query.get(id)
        if not category:
            api.abort(404, 'Category not found')
        for key, value in api.payload.items():
            setattr(category, key, value)
        db.session.commit()
        return category.to_dict(), 200

    @api.doc(responses={
        200: 'Успешный DELETE-запрос, категория удалена',
        400: 'Некорректный запрос',
        404: 'Категория не найдена'
    })
    @categoryNS.doc(security='jwt')
    def delete(self, id):
        """Delete category by ID"""
        category = Category.query.filter_by(id=id).first()
        if not category:
            api.abort(404, message='Категория с id {} не найдена'.format(id))
        try:
            db.session.delete(category)
            db.session.commit()
            return {'msg': 'Категория с id {} была удалена'.format(id)}, 200
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return {'msg': 'Ошибка.'}, 400

@categoryNS.doc(security='jwt')
class UploadCategoryPic(Resource):
    @categoryNS.doc(security='jwt')
    @categoryNS.expect(categoryNS.parser().add_argument('image', location='files', type='file'))
    def put(self, id):
        """Give picture for category by his ID"""
        category = Category.query.filter_by(id=id).first()
        if not category:
            categoryNS.abort(404, 'Профиль не найден')

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

        # Update category picture
        category.picture = response['link']
        db.session.commit()

        return category_schema.dump(category), 201
