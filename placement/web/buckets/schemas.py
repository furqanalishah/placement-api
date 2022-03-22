from marshmallow import Schema
from marshmallow.fields import Boolean, Nested, String

from placement.web.buckets.common.schemas import ResourceOutSchema


class BucketInSchema(Schema):
    name = String(required=True, description="Name for the Bucket Server.")
    description = String(description="Some more details about the Bucket Server.")


class BucketOutSchema(Schema):
    name = String(required=True, description="Name for the Bucket Server.")
    description = String(required=True, description="Some more details about the Bucket Server.")
    online = Boolean(required=True, description="Online status of the Bucket Server.")
    enabled = Boolean(required=True, description="Enabled status of the Bucket Server.")
    resources = Nested(ResourceOutSchema, many=True, required=True)
