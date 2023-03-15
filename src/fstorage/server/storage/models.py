from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import (
    BIGINT,
    Column,
    Field,
    SQLModel
)


class Metadata(SQLModel, table=True):
    """
    Metadata of the file placed in the storage.
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)

    upload_timestamp: float
    file_name: str
    file_hash: str
    file_size: int = Field(default=None, sa_column=Column(BIGINT))
