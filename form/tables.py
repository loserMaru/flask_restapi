from flask_restx import fields, Resource

from extensions import db
from extensions.flask_restx_extension import api, tableNS
from models import Tables
from schemas import TableSchema

table_schema = TableSchema()

table_model = tableNS.model('Table', {
    'id': fields.Integer(readonly=True),
    'number': fields.String,
    'seat': fields.String,
    'restaurant_id': fields.Integer,
})


class TableResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @tableNS.marshal_list_with(table_model)
    def get(self):
        tables = Tables.query.all()
        return tables, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресурса',
        400: 'Некорректный запрос'
    })
    @tableNS.expect(table_model)
    @tableNS.marshal_with(table_model, code=201)
    def post(self):
        table = Tables(**tableNS.payload)
        db.session.add(table)
        db.session.commit()
        return table.to_dict(), 201


class TableResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресурс не найден'
    })
    @tableNS.marshal_with(table_model)
    def get(self, id):
        table = Tables.query.filter_by(id=id).first()
        if not table:
            api.abort(404, 'Table not found')
        return table, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресурс не найден'
    })
    @tableNS.expect(table_model)
    def put(self, id):
        table = Tables.query.filter_by(id=id).first()
        if not table:
            api.abort(404, 'Table not found')
        for key, value in tableNS.payload.items():
            setattr(table, key, value)
        db.session.commit()
        return table_schema.dump(table), 200

    @api.doc(responses={
        204: 'Успешный DELETE-запрос, ресурс удален',
        404: 'Ресурс не найден'
    })
    def delete(self, id):
        table = Tables.query.filter_by(id=id).first()
        if not table:
            api.abort(404, message='Стол с id {} не найден'.format(id))
        db.session.delete(table)
        db.session.commit()
        return {'result': 'success'}, 204
