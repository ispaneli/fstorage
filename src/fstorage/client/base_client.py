from __future__ import annotations

from typing import BinaryIO
from uuid import UUID


class BaseFStorageClient:
    """
    Base FStorage-client class.
    """
    not_found_error = FileExistsError("The file with this ID doesn't exist.")

    def __init__(self, url: str):
        """
        Initialization of object.

        :param str url: Link to the FStorage server; type: "http://127.0.0.1:8000".
        """
        self._url = f"{url}/fstorage"

    def upload(self, file_bin_stream: BinaryIO) -> dict[str, str]:
        """
        Base UPLOAD-method.

        :param BinaryIO file_bin_stream: File stream to upload to the FStorage.
        :return: File ID; type: {'id': "<file_id>"}.
        :rtype: dict[str, str]
        """
        raise NotImplementedError

    def get(self, file_id: str | UUID) -> dict[str, str | bytes]:
        """
        Base GET-method.

        :param Union[str, UUID] file_id: File ID.
        :return: File data; type: {'filename': "LICENSE", 'bytes': '<data_as_bytes>'}.
        :rtype: dict[str, str | bytes]
        """
        raise NotImplementedError

    def delete(self, file_id: str | UUID) -> None:
        """
        Base DELETE-method.

        :param Union[str, UUID] file_id: File ID.
        :return: None
        """
        raise NotImplementedError
