from apiflask import input, output

from . import loads
from .schemas import LoadInSchema, LoadOutSchema


@loads.get("")
@output(LoadOutSchema)
def list_loads():
    return "List Load"


@loads.post("")
@input(LoadInSchema)
def add_load():
    return "Add Load"


@loads.get("/<load_id>")
@output(LoadOutSchema)
def get_load(load_id):
    return f"Get Load {load_id}"


@loads.delete("/<load_id>")
def delete_load(load_id):
    return f"Delete Load {load_id}"


@loads.patch("/<load_id>")
def update_load(load_id):
    return f"Update Load {load_id}"
