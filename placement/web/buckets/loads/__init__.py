from apiflask import APIBlueprint

loads = APIBlueprint("loads", __name__, "Loads", url_prefix="/loads")

from . import api
