import uuid
from sqlalchemy import Column, String, Integer, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import UUID
from db import Base
import datetime


class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    size = Column(Integer, nullable=False)
    url = Column(Text, nullable=False)
    upload_date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    storage_type = Column(String, nullable=False)
