import uuid

from sqlalchemy import Column, Enum, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from placement.models.base import Base


class Load(Base):
    ID_KEY = "id"
    NAME_KEY = "name"
    DESCRIPTION_KEY = "description"
    STATE_KEY = "state"
    WORKLOAD_SYSTEM_NAME_KEY = "workload_system_name"
    AVAILABLE_RAM_KEY = "available_ram"
    AVAILABLE_CPU_KEY = "available_cpu"
    AVAILABLE_HDD_KEY = "available_hdd"

    __tablename__ = "loads"

    LOAD_STATE_PENDING = "pending"
    LOAD_STATE_RUNNING = "running"
    LOAD_STATE_SUSPENDED = "suspended"
    LOAD_STATE_UPDATING = "updating"
    LOAD_STATE_STOPPED = "stopped"
    LOAD_STATE_ERROR = "error"

    ALL_LOAD_STATES_LIST = \
        [
            LOAD_STATE_PENDING, LOAD_STATE_RUNNING, LOAD_STATE_SUSPENDED, LOAD_STATE_UPDATING, LOAD_STATE_STOPPED,
            LOAD_STATE_ERROR
        ]
    id = Column(String(32), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    state = Column(Enum(*ALL_LOAD_STATES_LIST), default=LOAD_STATE_PENDING)
    __workload_system_name = Column('workload_system_name', String(255), nullable=False)

    bucket_id = Column(String(32), ForeignKey("buckets.id"))
    resources = relationship("Resource", backref="load", cascade="all, delete-orphan", lazy="dynamic")

    def __init__(self, name, workload_system_name, state=LOAD_STATE_PENDING, description=None):
        self.id = uuid.uuid4().hex
        self.name = name
        self.state = state
        self.description = description
        self.workload_system_name = workload_system_name

    @property
    def workload_system_name(self):
        return self.__workload_system_name

    @workload_system_name.setter
    def workload_system_name(self, name):
        self.__workload_system_name = name

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
            self.ID_KEY:self.id,
            self.NAME_KEY: self.name,
            self.DESCRIPTION_KEY: self.description,
            self.AVAILABLE_HDD_KEY: self.available_hdd,
            self.AVAILABLE_CPU_KEY: self.available_cpu,
            self.AVAILABLE_RAM_KEY: self.available_ram
        }
