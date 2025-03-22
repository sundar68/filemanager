from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID as uuid_lib


class FileBase(BaseModel):
    name: str
    type: str
    size: int
    url: str
    storage_type: Optional[str] = Field(default='minio')


class FileCreate(FileBase):
    pass


class FileUploadBody(BaseModel):
    name: str
    type: str
    size: int

class FileRead(FileBase):
    id: uuid_lib
    upload_date: datetime

    class Config:
        from_attributes = True
