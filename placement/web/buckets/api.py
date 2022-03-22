from apiflask import input, output

from placement.models import Bucket
from placement.web import db as placement_db
from . import buckets
from .schemas import BucketInSchema, BucketOutSchema


@buckets.get("")
@output(BucketOutSchema)
def list_buckets():
    return "List Bucket"


@buckets.post("")
@input(BucketInSchema)
@output(BucketOutSchema)
def add_bucket(data):
    bucket = Bucket(name=data["name"], description=data.get("description"))
    placement_db.session.add(bucket)
    placement_db.session.commit()
    return bucket.to_json()


@buckets.get("/<bucket_id>")
@output(BucketOutSchema)
def get_bucket(bucket_id):
    return f"Get Bucket {bucket_id}"


@buckets.delete("/<bucket_id>")
def delete_bucket(bucket_id):
    return f"Delete Bucket {bucket_id}"


@buckets.patch("/<bucket_id>")
def update_bucket(bucket_id):
    return f"Update Bucket {bucket_id}"
