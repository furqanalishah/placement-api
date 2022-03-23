from apiflask import input, output
from flask import Response

from placement.common import get_pagination_schema
from placement.common.schemas import PaginationQuerySchema
from placement.models import Bucket
from placement.web import db as placement_db
from placement.web.common.utils import get_paginated_response_json
from . import buckets
from .schemas import BucketInSchema, BucketOutSchema


@buckets.get("")
@input(PaginationQuerySchema, location="query")
@output(get_pagination_schema(BucketOutSchema))
def list_buckets(pagination_query_params):
    buckets_query = placement_db.session.query(Bucket)
    bucket_page = buckets_query.paginate(page=pagination_query_params["page"],
                                         per_page=pagination_query_params["per_page"],
                                         error_out=False)
    if not bucket_page.items:
        return Response(status=204)

    return get_paginated_response_json(
        items=[item.to_json() for item in bucket_page.items],
        pagination_obj=bucket_page
    )


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


@buckets.post("/db_seed")
def db_seed():
    from placement.models import Bucket, Resource, Load
    from placement.web import db

    buckets_list = [
        {
            "name": "bucket-1",
            "description": "Some dummy description for 'bucket-1'",
            "resources": [
                {
                    "element": "CPU",
                    "capacity": 40,
                    "utilisation": 10,
                    "type": "worker",
                },
                {
                    "element": "RAM",
                    "capacity": 50,
                    "utilisation": 10,
                    "type": "worker",
                },
                {
                    "element": "HDD",
                    "capacity": 500,
                    "utilisation": 50,
                    "type": "worker",
                }
            ],
            "loads": [
                {
                    "name": "vm-1",
                    "workload_system_name": "4897349-vm-1",
                    "resources": [
                        {
                            "element": "CPU",
                            "capacity": 10,
                            "utilisation": 0,
                            "type": "workload",
                        },
                        {
                            "element": "RAM",
                            "capacity": 10,
                            "utilisation": 0,
                            "type": "workload",
                        },
                        {
                            "element": "HDD",
                            "capacity": 50,
                            "utilisation": 0,
                            "type": "workload",
                        }
                    ]
                },

            ]
        },
        {
            "name": "bucket-2",
            "description": "Some dummy description for 'bucket-2'",
            "resources": [
                {
                    "element": "CPU",
                    "capacity": 30,
                    "utilisation": 10,
                    "type": "worker",
                },
                {
                    "element": "RAM",
                    "capacity": 40,
                    "utilisation": 10,
                    "type": "worker",
                },
                {
                    "element": "HDD",
                    "capacity": 300,
                    "utilisation": 50,
                    "type": "worker",
                }
            ],
            "loads": [
                {
                    "name": "vm-2",
                    "workload_system_name": "48748954-vm-2",
                    "resources": [
                        {
                            "element": "CPU",
                            "capacity": 10,
                            "utilisation": 0,
                            "type": "workload",
                        },
                        {
                            "element": "RAM",
                            "capacity": 10,
                            "utilisation": 0,
                            "type": "workload",
                        },
                        {
                            "element": "HDD",
                            "capacity": 50,
                            "utilisation": 0,
                            "type": "workload",
                        }
                    ]
                },

            ]
        },
        {
            "name": "bucket-3",
            "description": "Some dummy description for 'bucket-3'",
            "resources": [
                {
                    "element": "CPU",
                    "capacity": 50,
                    "utilisation": 20,
                    "type": "workload",
                },
                {
                    "element": "RAM",
                    "capacity": 50,
                    "utilisation": 16,
                    "type": "workload",
                },
                {
                    "element": "HDD",
                    "capacity": 500,
                    "utilisation": 20,
                    "type": "workload",
                }
            ]
        }
    ]
    db_session = db.session
    for bucket_json in buckets_list:
        bucket = Bucket(name=bucket_json["name"], description=bucket_json["description"])
        db_session.add(bucket)
        for resource_json in bucket_json["resources"]:
            resource_obj = Resource(
                capacity=resource_json["capacity"], utilisation=resource_json["utilisation"],
                element=resource_json["element"], type_=resource_json["type"]
            )
            bucket.resources.append(resource_obj)

        for load_json in bucket_json.get("loads", []):
            load_obj = Load(name=load_json["name"], workload_system_name=load_json["workload_system_name"])
            for load_resource_json in load_json.get("resources", []):
                load_resource_obj = Resource(
                    capacity=load_resource_json["capacity"], utilisation=load_resource_json["utilisation"],
                    element=load_resource_json["element"], type_=load_resource_json["type"]
                )
                load_obj.resources.append(load_resource_obj)
            bucket.loads.append(load_obj)

        db_session.commit()
    return "Done"
