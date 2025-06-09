"""Search-related models"""

from typing import Union
from .base import BaseBlockScoutModel

class SearchResultRedirect(BaseBlockScoutModel):
    """Search result redirect"""
    parameter: str
    redirect: bool
    type: str  # "address" | "block" | "transaction"

class SearchResultToken(BaseBlockScoutModel):
    """Search result token"""
    address: str
    address_url: str
    exchange_rate: str
    icon_url: Optional[str] = None
    is_smart_contract_verified: bool
    name: str
    symbol: str
    token_type: str
    token_url: str
    total_supply: str
    type: str  # always "token"

class SearchResultAddressOrContract(BaseBlockScoutModel):
    """Search result address or contract"""
    address: str
    is_smart_contract_verified: bool
    name: Optional[str] = None
    type: str  # "address" | "contract"
    url: str

class SearchResultBlock(BaseBlockScoutModel):
    """Search result block"""
    block_hash: str
    block_number: int
    timestamp: str
    type: str  # always "block"
    url: str

class SearchResultTransaction(BaseBlockScoutModel):
    """Search result transaction"""
    timestamp: str
    transaction_hash: str
    type: str  # always "transaction"
    url: str

SearchResult = Union[
    SearchResultToken,
    SearchResultAddressOrContract,
    SearchResultBlock,
    SearchResultTransaction
]