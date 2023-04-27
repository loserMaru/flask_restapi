from extensions import ma
from models import Tables


class TableSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tables
