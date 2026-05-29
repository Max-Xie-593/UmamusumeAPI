from __future__ import annotations

__all__ = (
    "UmaMusumeAPIError",
    "DataNotFoundError",
    "ConnectionTimeoutError"
)

class UmaMusumeAPIError(Exception):
    """Base exception class for Uma Musume API errors.

    Args:
        Exception (class): Base Exception Class
    """

    def __init__(self, code: int) -> None:
        self.code = code

    def __str__(self) -> str:
        return f"An error occurred while requesting the API, status code {self.code}"
    
class DataNotFoundError(UmaMusumeAPIError):
    """Exception raised when requested data is not found (404).

    Args:
        UmaMusumeAPIError (Class): Base class for Uma Musume API errors
    """

    def __init__(self) -> None:
        self.code = 404
    
    def __str__(self) -> str:
        return "Data not found"
    
class ConnectionTimeoutError(UmaMusumeAPIError):
    """Exception raised when the connection to the API times out (522).

    Args:
        UmaMusumeAPIError (Class): Base class for Uma Musume API errors
    """

    def __init__(self) -> None:
        self.code = 522

    def __str__(self) -> str:
        return "Connection to the API timed out"
