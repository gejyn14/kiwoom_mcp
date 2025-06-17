"""
Custom exceptions for Kiwoom MCP Server
"""


class KiwoomAPIError(Exception):
    """Base exception for Kiwoom API errors"""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError(KiwoomAPIError):
    """Authentication related errors"""
    pass


class OrderError(KiwoomAPIError):
    """Order execution related errors"""
    pass


class ConfigurationError(Exception):
    """Configuration related errors"""
    pass


class TokenExpiredError(AuthenticationError):
    """Token expired error"""
    pass 