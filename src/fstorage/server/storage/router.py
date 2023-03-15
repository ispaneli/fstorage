import hashlib
import os
from datetime import datetime

from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.fstorage.server.app_params import APP_PARAMS

from .exceptions import IntegrityError, NotFoundError
from .models import Metadata


ROUTER = APIRouter(tags=['File storage'], prefix="/fstorage")


@ROUTER.post("/")
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

    with open(APP_PARAMS.storage_path / f"{metadata.id}.bin", 'wb') as storage:
        storage.write(file_data)
    async with AsyncSession(APP_PARAMS.db_engine) as session:
        session.add(metadata)
        await session.commit()

    return response


@ROUTER.get("/{file_uuid}")
async def get(file_uuid: str) -> FileResponse:
    """
    Getting a file from storage.

    :param str file_uuid: UUID of existing file.
    :return: The file from storage as response.
    :rtype: FileResponse
    """
    # Check №1.
    filepath = APP_PARAMS.storage_path / f"{file_uuid}.bin"
    if not filepath.exists():
        raise NotFoundError

    with open(filepath, 'rb') as storage:
        file_data = storage.read()
    async with AsyncSession(APP_PARAMS.db_engine) as session:
        statement = select(Metadata).where(Metadata.id == file_uuid)
        metadata = (await session.execute(statement)).scalar()

    # Check №2.
    if any((
        metadata.file_size != len(file_data),
        metadata.file_hash != hashlib.sha1(file_data).hexdigest()
    )):
        raise IntegrityError

    return FileResponse(filepath, filename=metadata.file_name)


@ROUTER.delete("/{file_uuid}")
async def delete(file_uuid: str) -> None:
    """
    Deleting a file from storage.

    :param str file_uuid: UUID of existing file.
    :return: None
    """
    filepath = APP_PARAMS.storage_path / f"{file_uuid}.bin"
    if not filepath.exists():
        raise NotFoundError
    os.remove(filepath)

    async with AsyncSession(APP_PARAMS.db_engine) as session:
        statement = select(Metadata).where(Metadata.id == file_uuid)
        metadata = (await session.execute(statement)).scalar()
        await session.delete(metadata)
