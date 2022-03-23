from marshmallow import Schema
from marshmallow.fields import Boolean, Integer, Nested, String

from placement.web.buckets.common.schemas import ResourceOutSchema
from placement.web.buckets.loads.schemas import LoadOutSchema


class BucketInSchema(Schema):
    name = String(required=True, description="Name for the Bucket Server.")
    description = String(description="Some more details about the Bucket Server.")


class BucketOutSchema(Schema):
    id = String(required=True, description="UUID of the Bucket")
    name = String(required=True, description="Name for the Bucket Server.")
    description = String(required=True, description="Some more details about the Bucket Server.")
    online = Boolean(required=True, description="Online status of the Bucket Server.")
    enabled = Boolean(required=True, description="Enabled status of the Bucket Server.")
    available_ram = Integer(required=True, description="Available RAM")
    available_cpu = Integer(required=True, description="Available CPU")
    available_hdd = Integer(required=True, description="Available HDD")
    loads = Nested(LoadOutSchema, many=True, required=True)
    resources = Nested(ResourceOutSchema, many=True, required=True)
