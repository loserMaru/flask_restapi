from flask_restx import fields, Resource

from extensions import db
from extensions.flask_restx_extension import tableNS
from models.models import Tables

table_model = tableNS.model('Table', {
    'id': fields.Integer(readonly=True),
    'number': fields.String,
    'seat': fields.String,
    'restaurant_id': fields.Integer,
})


class TableResourceList(Resource):
    @tableNS.marshal_list_with(table_model)
    def get(self):
        tables = Tables.query.all()
        return tables

    @tableNS.expect(table_model)
    def post(self):
        table = Tables(**tableNS.payload)
        db.session.add(table)
        db.session.commit()
        return {'result': 'success'}


class TableResource(Resource):
    @tableNS.marshal_with(table_model)
    def get(self, table_id):
        table = Tables.query.filter_by(id=table_id).first()
        if not table:
            tableNS.abort(404, 'Table not found')
        return table

    @tableNS.expect(table_model)
    def put(self, table_id):
        table = Tables.query.filter_by(id=table_id).first()
        for key, value in tableNS.payload.items():
            setattr(table, key, value)
        db.session.commit()
        return {'result': 'success'}

    def delete(self, table_id):
        table = Tables.query.filter_by(id=table_id).first()
        if not table:
            tableNS.abort(404, 'Table not found')
        db.session.delete(table)
        db.session.commit()
        return {'result': 'success'}
