import hashlib
import os
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.db import ASYNC_DB_ENGINE
from models.metadata import Metadata

STORAGE_ROUTER = APIRouter(tags=['Storage'])
_STORAGE_PATH = Path(__file__).parents[1] / ".storage"

_EXISTING_ERROR = HTTPException(
    status_code=404,
    detail="This ID does not exist."
)
_INTEGRITY_ERROR = HTTPException(
    status_code=500,
    detail="The file was corrupted during storage."
)


@STORAGE_ROUTER.post("/upload")
async def upload(file: UploadFile) -> dict[str, str]:
    """
    Uploading a new file to storage.

    :param UploadFile file: New file sent by the Client.
    :return: UUID of the new file.
    :rtype: dict[str, str]
    """
    file_data: bytes = await file.read()
    metadata = Metadata(
        upload_timestamp=datetime.utcnow().timestamp(),
        file_name=file.filename,
        file_hash=hashlib.sha1(file_data).hexdigest(),
        file_size=len(file_data)
    )
    response = {'id': str(metadata.id)}

    with open(_STORAGE_PATH / f"{metadata.id}.bin", 'wb') as storage:
        storage.write(file_data)
    async with AsyncSession(ASYNC_DB_ENGINE) as session:
        session.add(metadata)
        await session.commit()

    return response


@STORAGE_ROUTER.get("/get/{file_uuid}")
async def get(file_uuid: str) -> FileResponse:
    """
    Getting a file from storage.

    :param str file_uuid: UUID of existing file.
    :return: The file from storage as response.
    :rtype: FileResponse
    """
    # Check №1.
    filepath = _STORAGE_PATH / f"{file_uuid}.bin"
    if not filepath.exists():
        raise _EXISTING_ERROR

    with open(filepath, 'rb') as storage:
        file_data = storage.read()
    async with AsyncSession(ASYNC_DB_ENGINE) as session:
        statement = select(Metadata).where(Metadata.id == file_uuid)
        metadata = (await session.execute(statement)).scalar()

    # Check №2.
    if metadata.file_size != len(file_data) or metadata.file_hash != hashlib.sha1(file_data).hexdigest():
        raise _INTEGRITY_ERROR

    return FileResponse(filepath, filename=metadata.file_name)


@STORAGE_ROUTER.delete("/delete/{file_uuid}")
async def delete(file_uuid: str) -> None:
    """
    Deleting a file from storage.

    :param str file_uuid: UUID of existing file.
    :return: None
    """
    filepath = _STORAGE_PATH / f"{file_uuid}.bin"
    if not filepath.exists():
        raise _EXISTING_ERROR
    os.remove(filepath)

    async with AsyncSession(ASYNC_DB_ENGINE) as session:
        statement = select(Metadata).where(Metadata.id == file_uuid)
        metadata = (await session.execute(statement)).scalar()
        await session.delete(metadata)
