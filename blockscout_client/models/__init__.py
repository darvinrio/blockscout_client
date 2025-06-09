"""Models package"""

from .base import BaseBlockScoutModel, PaginatedResponse
from .address import *
from .transaction import *
from .token import *
from .block import *
from .search import *

# Update forward references
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass
else:
    # Update forward references for circular imports
    TokenTransfer.model_rebuild()
    Transaction.model_rebuild()
    NFTInstance.model_rebuild()
    Address.model_rebuild()