from apiflask import APIBlueprint

from ..buckets.loads import loads as loads_blueprint

buckets = APIBlueprint("buckets", __name__, "Buckets", url_prefix="/api/buckets")
buckets.register_blueprint(loads_blueprint)

from . import api
