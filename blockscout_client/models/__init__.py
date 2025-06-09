"""Models package"""

# Import base models first
from .base import (
    BaseBlockScoutModel,
    PaginatedResponse,
    AddressTag,
    WatchlistName,
    AddressParam,
    TokenInfo,
)

# Import other models
from .address import *
from .transaction import *
from .token import *
from .block import *
from .search import *


# Rebuild models to resolve forward references
def _rebuild_models():
    """Rebuild models to resolve forward references"""
    import sys
    from pydantic import BaseModel

    current_module = sys.modules[__name__]

    for name in dir(current_module):
        obj = getattr(current_module, name)
        if (
            isinstance(obj, type)
            and issubclass(obj, BaseModel)
            and obj is not BaseModel
        ):
            try:
                obj.model_rebuild()
            except Exception:
                pass  # Some models might not need rebuilding


# Rebuild models after all imports
_rebuild_models()
