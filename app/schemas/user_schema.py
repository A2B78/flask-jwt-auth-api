from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, load_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    role = fields.Str()

user_schema = UserSchema()
user_schema_public = UserSchema(exclude=["password"])