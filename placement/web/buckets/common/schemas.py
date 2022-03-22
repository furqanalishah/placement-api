from marshmallow import Schema
from marshmallow.fields import Integer, String


class ResourceOutSchema(Schema):
    element = String(required=True)
    capacity = Integer(required=True)
    utilisation = Integer(required=True)
    type_ = String(data_key="type", required=True)
