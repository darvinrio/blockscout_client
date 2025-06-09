"""Custom exceptions for BlockScout API client"""

class BlockScoutError(Exception):
    """Base exception for BlockScout client"""
    pass

class BlockScoutAPIError(BlockScoutError):
    """Exception raised for API errors"""
    
    def __init__(self, status_code: int, message: str, response_data: dict = None):
        self.status_code = status_code
        self.message = message
        self.response_data = response_data or {}
        super().__init__(f"API Error {status_code}: {message}")