"""BlockScout API Client Package"""

from .client import BlockScoutClient
from .models import *
from .exceptions import BlockScoutError, BlockScoutAPIError

__version__ = "1.0.0"
__all__ = ["BlockScoutClient", "BlockScoutError", "BlockScoutAPIError"]
