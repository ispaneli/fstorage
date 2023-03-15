from fastapi import HTTPException


class IntegrityError(HTTPException):
    """
    Storage exception for violation of integrity of file.
    """
    status_code = 500
    detail = "The file with this ID was corrupted during storage."

    def __init__(self):
        """
        Initialization using init-method of parent class
        `fastapi.HTTPException.__init__.py(status_code=<...>, detail=<...>)`.
        """
        super().__init__(
            status_code=self.status_code,
            detail=self.detail
        )


class NotFoundError(HTTPException):
    """
    Storage exception for nonexistent files.
    """
    status_code = 404
    detail = "The file with this ID doesn't exist."

    def __init__(self):
        """
        Initialization using init-method of parent class
        `fastapi.HTTPException.__init__.py(status_code=<...>, detail=<...>)`.
        """
        super().__init__(
            status_code=self.status_code,
            detail=self.detail
        )


