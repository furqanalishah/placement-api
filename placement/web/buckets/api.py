from . import buckets


@buckets.get("/buckets")
def list_buckets():
    return " Buckets"
