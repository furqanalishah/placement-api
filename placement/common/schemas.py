from marshmallow import Schema
from marshmallow.fields import Integer, Nested
from marshmallow.validate import Range

from config import PaginationConfig


def get_pagination_schema(schema):
    class PaginatedResponseSchema(Schema):
        items = Nested(schema, many=True, dump_only=True, required=True)
        previous_page = Integer(required=True, description="Previous page number")
        next_page = Integer(required=True, description="Next page number")
        total_pages = Integer(required=True, description="Total pages")

    return PaginatedResponseSchema


class PaginationQuerySchema(Schema):
    page = Integer(missing=1)
    per_page = Integer(
        missing=PaginationConfig.DEFAULT_ITEMS_PER_PAGE, validate=Range(1, PaginationConfig.MAX_ITEMS_PER_PAGE)
    )
