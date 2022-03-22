import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String, Text
from sqlalchemy.orm import backref, relationship

from placement.models.base import Base


class Bucket(Base):
    __tablename__ = "buckets"

    id = Column(String(32), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    enabled = Column(Boolean, nullable=False, default=True)
    online = Column(Boolean, nullable=False, default=True)
    last_seen = Column(DateTime, default=datetime.utcnow())

    loads = relationship("Load", backref=backref("bucket", cascade="all, delete-orphan", lazy="dynamic"))
    resources = relationship("Resource", backref=backref("load", cascade="all, delete-orphan", lazy="dynamic"))

    def __init__(self, name, enabled=True, online=True, description=None, last_seen=None):
        self.id = uuid.uuid4().hex
        self.name = name
        self.enabled = enabled
        self.online = online
        self.last_seen = last_seen
        self.description = description
