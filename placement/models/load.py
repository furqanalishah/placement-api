import uuid

from sqlalchemy import Column, Enum, ForeignKey, String, Text
from sqlalchemy.orm import backref, relationship

from placement.models.base import Base


class Load(Base):
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
    resources = relationship("Resource", backref=backref("load", cascade="all, delete-orphan", lazy="dynamic"))

    def __init__(self, name, state, workload_system_name, description=None):
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
