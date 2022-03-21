from apiflask import APIBlueprint

buckets = APIBlueprint("buckets", __name__, "Buckets")

from . import api
