from marshmallow import Schema
from marshmallow.fields import Nested, String
from marshmallow.validate import OneOf

from placement.models import Load


class LoadInSchema(Schema):
    name = String(required=True, description="Name for the Workload.")
    description = String(description="Some more details about the Workload.")
    resources = Nested("ResourceOutSchema", many=True, required=True)


class LoadOutSchema(Schema):
    name = String(required=True, description="Name for the Workload.")
    description = String(required=True, description="Some more details about the Workload.")
    state = String(required=True, description="State of the Workload", validate=OneOf(Load.ALL_LOAD_STATES_LIST))
    resources = Nested("ResourceOutSchema", many=True, required=True)
