from marshmallow import Schema, fields
from .models import FirstModel

class FirstModelSchema(Schema):
    id = fields.Int(dump_only=True)
    parent_id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    created_at = fields.Date()
    updated_at = fields.Date()


firstmodel_schema = FirstModelSchema()
firstmodel_schemas = FirstModelSchema(many=True)
