class AppException(Exception):
    """Base exception for application."""
    pass

class GraphAPIException(AppException):
    """Exception raised for errors in the Graph API."""
    def __init__(self, status_code: int, message: str, details: dict = None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(f"Graph API Error {status_code}: {message}")

class AuthException(AppException):
    """Exception raised for authentication errors."""
    pass

class ConfigurationException(AppException):
    """Exception raised for configuration errors."""
    pass
