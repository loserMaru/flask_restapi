from flask_restx import fields, Resource

from extensions import db, jwt_required_class
from extensions.flask_restx_extension import api, tableNS
from models import Tables
from schemas import TableSchema

table_schema = TableSchema()

table_model = tableNS.model('Table', {
    'id': fields.Integer(readonly=True),
    'number': fields.String(required=True),
    'seat': fields.String(required=True),
    'restaurant_id': fields.Integer(required=True),
})


@jwt_required_class
class TableResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @tableNS.doc(security='jwt')
    @tableNS.marshal_list_with(table_model)
    def get(self):
        """Get a list of tables"""
        tables = Tables.query.all()
        return tables, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресурса',
        400: 'Некорректный запрос'
    })
    @tableNS.expect(table_model)
    @tableNS.doc(security='jwt')
    @tableNS.marshal_with(table_model, code=201)
    def post(self):
        """Create new table"""
        table = Tables(**tableNS.payload)
        db.session.add(table)
        db.session.commit()
        return table.to_dict(), 201


@jwt_required_class
class TableResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресурс не найден'
    })
    @tableNS.doc(security='jwt')
    @tableNS.marshal_with(table_model)
    def get(self, id):
        """Get table with id"""
        table = Tables.query.filter_by(id=id).first()
        if not table:
            api.abort(404, 'Table not found')
        return table, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресурс не найден'
    })
    @tableNS.doc(security='jwt')
    @tableNS.expect(table_model)
    def put(self, id):
        """Edit table by id"""
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
    @tableNS.doc(security='jwt')
    def delete(self, id):
        """Delete table by id"""
        table = Tables.query.filter_by(id=id).first()
        if not table:
            api.abort(404, message='Стол с id {} не найден'.format(id))
        db.session.delete(table)
        db.session.commit()
        return {'result': 'success'}, 204
