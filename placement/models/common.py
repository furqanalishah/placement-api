import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text

from placement.models.base import Base


class Resource(Base):
    ID_KEY = "id"
    ELEMENT_KEY = "element"
    CAPACITY_KEY = "capacity"
    UTILISATION_KEY = "utilisation"
    TYPE_KEY = "type"

    __tablename__ = "resources"

    RESOURCE_TYPE_WORKLOAD = "workload"
    RESOURCE_TYPE_WORKER = "worker"

    ALL_RESOURCE_TYPES_LIST = [RESOURCE_TYPE_WORKLOAD, RESOURCE_TYPE_WORKER]

    id = Column(String(32), primary_key=True, index=True)
    element = Column(Text)  # TODO: Nullable?
    capacity = Column(Integer, nullable=False)
    utilisation = Column(Integer, nullable=False)
    # unit_type = ?? # TODO: Enum or free text?
    type_ = Column('type', Enum(*ALL_RESOURCE_TYPES_LIST))

    load_id = Column(String(32), ForeignKey("loads.id"))
    bucket_id = Column(String(32), ForeignKey("buckets.id"))

    def __init__(self, capacity, utilisation, element, type_):
        self.id = uuid.uuid4().hex
        self.capacity = capacity
        self.utilisation = utilisation
        self.element = element
        self.type_ = type_

    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.ELEMENT_KEY: self.element,
            self.CAPACITY_KEY: self.capacity,
            self.UTILISATION_KEY: self.utilisation,
            self.TYPE_KEY: self.type_
        }
