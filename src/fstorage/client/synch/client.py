from __future__ import annotations

from typing import BinaryIO
from uuid import UUID

import requests

from ..base_client import BaseFStorageClient


class SyncClient(BaseFStorageClient):
    """
    Synchronous FStorage-client class.
    """
    def upload(self, file_bin_stream: BinaryIO) -> dict[str, str]:
        """
        Synchronous UPLOAD-method.

        :param BinaryIO file_bin_stream: File stream to upload to the FStorage.
        :return: File ID; type: {'id': "<file_id>"}.
        :rtype: dict[str, str]
        """
        response = requests.post(
            self._url,
            files={
                'file': file_bin_stream,
            }
        )

        return response.json()

    def get(self, file_id: str | UUID) -> dict[str, str | bytes]:
        """
        Synchronous GET-method.

        :param Union[str, UUID] file_id: File ID.
        :return: File data; type: {'filename': "LICENSE", 'bytes': '<data_as_bytes>'}.
        :rtype: dict[str, str | bytes]
        """
        response = requests.get(f"{self._url}/{file_id}")

        if response.status_code == 404:
            raise self.not_found_error

        attachment = response.headers['content-disposition']
        return {
            'filename': attachment.split("filename=")[1][1:-1],
            'bytes': response.content
        }

    def delete(self, file_id: str | UUID) -> None:
        """
        Synchronous DELETE-method.

        :param Union[str, UUID] file_id: File ID.
        :return: None
        """
        response = requests.delete(f"{self._url}/{file_id}")

        if response.status_code == 404:
            raise self.not_found_error
