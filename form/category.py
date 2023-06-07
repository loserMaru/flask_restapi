from flask_restx import Resource, fields

from extensions import api, db, jwt_required_class
from extensions.flask_restx_extension import categoryNS
from models import Category

category_model = categoryNS.model('Category', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
})


@jwt_required_class
class CategoryResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @categoryNS.doc(security='jwt')
    @api.marshal_list_with(category_model)
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
        204: 'Успешный DELETE-запрос, категория удалена',
        404: 'Категория не найдена'
    })
    @categoryNS.doc(security='jwt')
    def delete(self, id):
        """Delete category by ID"""
        category = Category.query.get(id)
        if not category:
            api.abort(404, message='Категория с id {} не найдена'.format(id))
        db.session.delete(category)
        db.session.commit()
        return {'result': 'success'}, 204
