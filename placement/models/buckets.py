from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from placement.models.base import Base


class Bucket(Base):
    __tablename__ = "buckets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    enabled = Column(Boolean, nullable=False, default=True)
    online = Column(Boolean, nullable=False, default=True)
    last_seen = Column(DateTime)


class BucketResource(Base):
    __tablename__ = "bucket_resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    element = Column(Text)  # TODO: Nullable?
    capacity = Column(Integer, nullable=False)
    utilisation = Column(Integer, nullable=False)
    # unit_type = ?? # TODO: Enum or free text?
