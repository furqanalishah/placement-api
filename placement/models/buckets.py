import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String, Text
from sqlalchemy.orm import relationship

from placement.models.base import Base


class Bucket(Base):
    ID_KEY = "id"
    NAME_KEY = "name"
    DESCRIPTION_KEY = "description"
    ENABLED_KEY = "enabled"
    ONLINE_KEY = "online"
    LAST_SEEN_KEY = "last_seen"
    RESOURCES_KEY = "resources"
    LOADS_KEY = "loads"
    AVAILABLE_RAM_KEY = "available_ram"
    AVAILABLE_CPU_KEY = "available_cpu"
    AVAILABLE_HDD_KEY = "available_hdd"

    __tablename__ = "buckets"

    id = Column(String(32), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    enabled = Column(Boolean, nullable=False, default=True)
    online = Column(Boolean, nullable=False, default=True)
    last_seen = Column(DateTime, default=datetime.utcnow())

    loads = relationship("Load", backref="bucket", cascade="all, delete-orphan", lazy="dynamic")
    resources = relationship("Resource", backref="bucket", cascade="all, delete-orphan", lazy="dynamic")

    def __init__(self, name, enabled=True, online=True, description=None, last_seen=None):
        self.id = uuid.uuid4().hex
        self.name = name
        self.enabled = enabled
        self.online = online
        self.last_seen = last_seen
        self.description = description

    @property
    def RAM_resources(self):
        return self.resources.filter_by(element="RAM").all()

    @property
    def CPU_resources(self):
        return self.resources.filter_by(element="CPU").all()

    @property
    def HDD_resources(self):
        return self.resources.filter_by(element="HDD").all()

    @property
    def available_ram(self):
        return sum([(ram.capacity - ram.utilisation) for ram in self.RAM_resources])

    @property
    def available_cpu(self):
        return sum([(cpu.capacity - cpu.utilisation) for cpu in self.CPU_resources])

    @property
    def available_hdd(self):
        return sum([(hdd.capacity - hdd.utilisation) for hdd in self.HDD_resources])

    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.NAME_KEY: self.name,
            self.DESCRIPTION_KEY: self.description,
            self.ENABLED_KEY: self.enabled,
            self.ONLINE_KEY: self.online,
            self.LAST_SEEN_KEY: self.last_seen,
            self.AVAILABLE_RAM_KEY: self.available_ram,
            self.AVAILABLE_CPU_KEY: self.available_cpu,
            self.AVAILABLE_HDD_KEY: self.available_hdd,
            self.LOADS_KEY: [load.to_json() for load in self.loads.all()],
            self.RESOURCES_KEY: [resource_.to_json() for resource_ in self.resources.all()]
        }
