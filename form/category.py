from flask_restx import Resource, fields

from extensions import api, db
from extensions.flask_restx_extension import categoryNS
from models import Category

category_model = categoryNS.model('Category', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
})


class CategoryResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @api.marshal_list_with(category_model)
    def get(self):
        categories = Category.query.all()
        return categories, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание новой категории',
        400: 'Некорректный запрос'
    })
    @api.expect(category_model)
    @api.marshal_with(category_model, code=201)
    def post(self):
        category = Category(**api.payload)
        db.session.add(category)
        db.session.commit()
        return category.to_dict(), 201


class CategoryResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Категория не найдена'
    })
    @api.marshal_with(category_model)
    def get(self, id):
        category = Category.query.get(id)
        if not category:
            api.abort(404, 'Category not found')
        return category, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Категория не найдена'
    })
    @api.expect(category_model)
    def put(self, id):
        category = Category.query.get(id)
        if not category:
            api.abort(404, 'Category not found')
        for key, value in api.payload.items():
            setattr(category, key, value)
        db.session.commit()
        return category.to_dict(), 200

    @api.doc(responses={
        204: 'Успешный DELETE-запрос, категория удалена',
        404: 'Категория не найдена'
    })
    def delete(self, id):
        category = Category.query.get(id)
        if not category:
            api.abort(404, message='Категория с id {} не найдена'.format(id))
        db.session.delete(category)
        db.session.commit()
        return {'result': 'success'}, 204
