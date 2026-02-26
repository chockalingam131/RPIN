"""
Custom exceptions for RPIN application
"""
from typing import Any, Optional


class RPINException(Exception):
    """Base exception for RPIN application"""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class ValidationError(RPINException):
    """Raised when input validation fails"""
    pass


class DataNotFoundError(RPINException):
    """Raised when required data is not found"""
    pass


class ExternalAPIError(RPINException):
    """Raised when external API call fails"""
    pass


class ModelError(RPINException):
    """Raised when ML model prediction fails"""
    pass


class ConfigurationError(RPINException):
    """Raised when configuration is invalid"""
    pass


class DatabaseError(RPINException):
    """Raised when database operation fails"""
    pass
