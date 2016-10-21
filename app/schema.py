from marshmallow import Schema, fields

class EntitySchema(Schema):
    id = fields.Int(dump_only=True)
    parent_id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    created_at = fields.Date()
    updated_at = fields.Date()


entity_schema = EntitySchema()
entity_schemas = EntitySchema(many=True)
