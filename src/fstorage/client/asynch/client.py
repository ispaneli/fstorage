from __future__ import annotations

from typing import BinaryIO
from uuid import UUID

import aiohttp

from ..base_client import BaseFStorageClient


class AsyncClient(BaseFStorageClient):
    """
    Asynchronous FStorage-client class.
    """
    async def upload(self, file_bin_stream: BinaryIO) -> dict[str, str]:
        """
        Asynchronous UPLOAD-method.

        :param BinaryIO file_bin_stream: File stream to upload to the FStorage.
        :return: File ID; type: {'id': "<file_id>"}.
        :rtype: dict[str, str]
        """
        data = {'file': file_bin_stream.read()}

        async with aiohttp.ClientSession() as session:
            async with session.post(self._url, data=data) as response:
                return await response.json()

    async def get(self, file_id: str | UUID) -> dict[str, str | bytes]:
        """
        Asynchronous GET-method.

        :param Union[str, UUID] file_id: File ID.
        :return: File data; type: {'filename': "LICENSE", 'bytes': '<data_as_bytes>'}.
        :rtype: dict[str, str | bytes]
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._url}/{file_id}") as response:
                if response.status == 404:
                    raise self.not_found_error

                attachment = response.headers['content-disposition']
                return {
                    'filename': attachment.split("filename=")[1][1:-1],
                    'bytes': await response.text()
                }

    async def delete(self, file_id: str | UUID) -> None:
        """
        Asynchronous DELETE-method.

        :param Union[str, UUID] file_id: File ID.
        :return: None
        """
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{self._url}/{file_id}") as response:
                if response.status == 404:
                    raise self.not_found_error
