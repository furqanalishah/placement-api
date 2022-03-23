def get_paginated_response_json(items, pagination_obj):
    return {
        "items": items,
        "previous_page": pagination_obj.prev_num if pagination_obj.has_prev else None,
        "next_page": pagination_obj.next_num if pagination_obj.has_next else None,
        "total_pages": pagination_obj.pages
    }
